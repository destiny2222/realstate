from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login,logout
from .forms import  *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
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
            messages.success(request, "password_reset successful."    + user)
            
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
        form = ProfileUpdateForm(data=request.POST or None,instance=request.user, files=request.FILES )
        
        if form.is_valid():
            form.save()
            messages.success(request,'your profile is set')
            return redirect('index:profile')
        else:
            messages.error(request,  form.errors)
    return render(request, 'account/profile.html')  

@login_required(login_url='index:login') 
def logout_View(request):
	logout(request)

	return redirect('index:login')