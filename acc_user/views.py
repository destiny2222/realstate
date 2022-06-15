from dataclasses import fields
from django.http import Http404
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login,logout
from real.models import Bookmarklisting, Listing
from .forms import  *
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail, BadHeaderError
from django.views.generic import  UpdateView
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

# User = get_user_model()




def LoginView(request):
    form = Loginform()
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)
                request.session['username'] = username
                return redirect('index:dashborad')
        else:
            messages.success(request, "Incorrect Username or Password")
            form = Loginform(None)
            return redirect('index:login')
    return render(request, 'account/login.html', {'form':form})


def RegisterView(request):
    form = Signupform()
    if request.method == "POST":
        form = Signupform(request.POST or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
        
            return redirect("index:dashborad")
        else:
            password = form.data['password']
            password2 = form.data['confirm_password']
            for msg in form.errors.as_data():
                if msg == 'confirm_password' and password == password2:
                    messages.error(request, f"Selected password: {password} is not strong enough")
                elif msg == 'password2' and password != password2:
                    messages.error(request, f"Password: '{password}' and Confirmation Password: '{password2}' do not match")
            # messages.error(request,  form.errors)      
    return render(request, 'account/signup.html', {"form": form})

@login_required(login_url='index:login') 
def dashboardview(request):
    
    return render(request, 'account/dashboard.html') 

@login_required(login_url='index:login') 
def Myprofileview(request):
    form = ProfileUpdateForm()
    if request.method == 'POST':
        form = ProfileUpdateForm(data=request.POST or None,instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'your profile is updated')
            return redirect('index:dashborad')
        else:
            messages.error(request,  form.errors)
    return render(request, 'account/profile.html')  

@login_required(login_url='index:login') 
def logout_View(request):
	logout(request)

	return redirect('index:login')



def mypropertyView(request):
    mylist = Listing.objects.all()
    content = {'list':mylist}
    return render(request, 'account/my-property.html', content)


def bookmarklistview(request):
    list = Bookmarklisting.objects.filter(users=request.user)
    content = {'list': list}
    return render(request, 'account/bookmark-list.html', content)    

@login_required(login_url='/login/')
def bookmark(request, slug):
    bookmark = Listing.objects.get(id=slug)
    Bookmarklisting.objects.create(property=bookmark, users=request.user)
    return redirect('index:booklist')


# @login_required(login_url='/login/')
# def booklist_increment(request, slug):
#     qr = Bookmarklisting.objects.get(users=request.user, id=slug)
#     qr.quantity = qr.quantity + 1
#     qr.save()
#     return redirect('index:booklist')

# @login_required(login_url='/login/')
# def booklist_decrement(request, slug):
#     qr = Bookmarklisting.objects.get(users=request.user, id=slug)
#     if qr.quantity >=1:
#         qr.quantity = qr.quantity - 1
#         qr.save()
#     return redirect('index:booklist')

@login_required(login_url='/login/')
def booklist_delete(request, slug):
    qs = Bookmarklisting.objects.get(users=request.user, id=slug)
    qs.delete()
    return redirect('index:booklist')

class changepassword(PasswordChangeView):
    form_class = Changepasswordform
    template_name = 'account/change-password.html'
    success_url = reverse_lazy('index:password_success')   


def change_success(request):

    return render(request, 'account/change_success.html')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')    



def agentview(request, slug):
    # agent_obj =  get_object_or_404(Agent,pk=slug)
    agent_obj = CustomUser.objects.filter(pk=slug)
    if agent_obj.exists():
        agent_obj = CustomUser.objects.get(pk=slug)
    else:
        return redirect("index:404")
    verify_form = VerifyAgentForm()
    if request.method == 'POST':
        verify_form = VerifyAgentForm(request.POST)
        if verify_form.is_valid():
            gent = verify_form.save(commit=False)
            gent.user_agent = agent_obj
            # add user instance
            gent.user = request.user
            gent.save()
            messages.info(request, f"Submitte Successful under going  check by adminitrator, Please kindly return back to your profile,")
            return redirect('index:agent_page')
        else:
            verify_form = VerifyAgentForm()  
            messages.error(request, verify_form.errors)
    return render(request, 'account/add-agent.html', {'verify_form':verify_form})

  

def agentdashboard(request):

    return render(request, 'account/agent-suc.html')


def admindashboard(request):
    total_count = User.objects.all().count()
    count = User.objects.filter(last_login__startswith=timezone.now().date()).count()
    context = {'count':count, 'total_count':total_count}
    return render(request, 'admin/index.html', context)
  