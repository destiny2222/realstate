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
# Create your views here.

User = get_user_model()

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(username, password)
        if user != None:
            login(request, user)
            return redirect('index:home')
        else:
            messages.success(request, 'There is an error loging in.')
            return redirect('index:login')
    return render(request, 'account/login.html', {})


def RegisterView(request):
    form = Signupform()
    if request.method == "POST":
        form = Signupform(request.POST or None)
        if form.is_valid():
            form.save()
            # profile.objects.create(user=form)
            user = form.cleaned_data.get('username')
            messages.success(request, "Account Created successful.")
            
            return redirect("index:login")
        else:
            messages.error(request,  form.errors)
            # messages.error(request, "Unsuccessful password_reset. Invalid information.")      
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
            messages.success(request,'your profile is set')
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




