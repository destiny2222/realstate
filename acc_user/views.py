from django.http import Http404
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login,logout
from real.models import Bookmarklisting, Listing
from .forms import  *
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail, BadHeaderError
from django.views.generic import  UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,force_text,DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading

# Create your views here.

# User = get_user_model()

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authentication/activate.html',{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_HOST_USER,
                         to=[user.email]
                         )
    EmailThread(email).start()    


def LoginView(request):
    form = Loginform()
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user and not user.is_email_verified:
                messages.add_message(request, messages.ERROR,
                    'Email is not verified, please check your email inbox')
                return render(request, 'account/login.html')
            if not user:
                messages.add_message(request, messages.ERROR,
                                 'Incorrect Email or Password, try again')
                return render(request, 'account/login.html')
            login(request, user)
            messages.add_message(request, messages.SUCCESS,f'Welcome {user.username}')
            return redirect(reverse('index:dashboard'))
            # if user != None:
            #     login(request, user)
            #     request.session['username'] = username
                # return redirect('index:dashborad')
        else:
            form = Loginform(None)
            return redirect('index:login')
    return render(request, 'account/login.html', {'form':form})


def RegisterView(request):
    form = Signupform()
    if request.method == "POST":
        form = Signupform(request.POST or None)
        if form.is_valid():
            user = form.save()
            user.save()
            send_activation_email(user, request)
            messages.add_message(request, messages.SUCCESS,
                                 'We sent you an email to verify your account')
            return redirect("index:login")
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
    list = Bookmarklisting.objects.filter(user=request.user)
    content = {'list': list}
    return render(request, 'account/bookmark-list.html', content)    

@login_required(login_url='/login/')
def bookmark(request, slug):
    bookmark = Listing.objects.get(id=slug)
    if (Bookmarklisting.objects.filter(user=request.user) and Bookmarklisting.objects.filter(property=bookmark)).exists():
        print("Item is exists")
        messages.success(request, f"Bookmark already exists for this property")
        return redirect("index:property_details", slug=bookmark.slug)
    else:
        Bookmarklisting.objects.get_or_create(user=request.user, property=bookmark)
    
    # Bookmarklisting.objects.create(property=bookmark, mark=request.user)
    return redirect('index:booklist')

@login_required(login_url='/login/')
def booklist_delete(request, slug):
    qs = Bookmarklisting.objects.get(user=request.user, id=slug)
    qs.delete()
    return redirect('index:booklist')

# deleted = Wishlist.objects.filter(user=user, product=product).delete()
#     if deleted == 0:
#         # Can do something when nothing was deleted if you like
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



class changepassword(SuccessMessageMixin,PasswordChangeView):
    form_class = Changepasswordform
    template_name = 'account/change-password.html'
    success_url = reverse_lazy('index:password_success')
    success_message = 'Your Password as been change Successful!!!!'   


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
  



#   def signup(request):
#     if (request.method == 'POST'):
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         st = request.POST.get('student')
#         te = request.POST.get('teacher')
        
#         user = User.objects.create_user(
#             email=email,
#         )
#         user.set_password(password)
#         user.save()
        
#         usert = None
#         if st:
#             usert = user_type(user=user,is_student=True)
#         elif te:
#             usert = user_type(user=user,is_teach=True)
        
#         usert.save()
#         #Successfully registered. Redirect to homepage
#         return redirect('home')
#     return render(request, 'register.html')
    
# def login(request):
#     if (request.method == 'POST'):
#         email = request.POST.get('email') #Get email value from form
#         password = request.POST.get('password') #Get password value from form
#         user = authenticate(request, email=email, password=password)
        
#         if user is not None:
#             login(request, user)
#             type_obj = user_type.objects.get(user=user)
#             if user.is_authenticated and type_obj.is_student:
#                 return redirect('shome') #Go to student home
#             elif user.is_authenticated and type_obj.is_teach:
#                 return redirect('thome') #Go to teacher home
#         else:
#             # Invalid email or password. Handle as you wish
#             return redirect('home')

#     return render(request, 'home.html')


def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('login'))

    return render(request, 'authentication/activate-failed.html', {"user": user})