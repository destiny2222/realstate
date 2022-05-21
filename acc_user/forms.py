from dataclasses import field
from django import forms
from django.contrib.auth import  get_user_model,authenticate
from django.contrib.auth.forms import PasswordChangeForm

from real.models import CustomUser

User = get_user_model()

typeofuser = [
            ('As Customer', 'As Customer'),
            ('As Agent', 'As Agent'),
            ('As Agency', 'As Agency'),
    ]

class Loginform(forms.Form):
    username = forms.CharField()
    password = forms.CharField( widget=forms.PasswordInput)
    
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(Loginform, self).clean(*args, **kwargs) 



class Signupform(forms.Form):

    fullname = forms.CharField(widget=forms.TextInput(attrs={
         'class':'form-control',
         'type':'text',
         'id': 'fullname',
         'name': 'fullname',
         'placeholder': 'Full Name',
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
         'class':'form-control',
         'type':'email',
         'id': 'email',
         'name': 'email',
         'placeholder': 'Email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
         'class':'form-control',
         'type':'text',
         'id': 'username',
         'name': 'username',
         'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
         'class':'form-control',
         'type':'password',
         'id': 'password',
         'name': 'password',
         'placeholder': '*******',
    }))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs={
         'class':'form-control',
         'type':'text',
         'id': 'phone',
         'name': 'phone',
         'placeholder': '123 546 5847',
    }))
    register_as = forms.ChoiceField(choices=typeofuser,widget=forms.Select(attrs={
        'class':'form-control',
    }))

    def clean_fullname(self):
        fullname = self.cleaned_data['fullname'].lower()
        qs = User.objects.filter(fullname=fullname)
        if qs.count():
            raise forms.ValidationError("Name already exists")
        return fullname

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        qp = User.objects.filter(username=username)
        if qp.count():
            raise forms.ValidationError("Username already exist")
        return username
    
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  forms.ValidationError("Email already exists")
        return email
    
    def clean_number(self):
        phonenumber = self.cleaned_data['phone_field'].lower()
        r = User.objects.filter(phonenumber=phonenumber)
        if r.count():
            raise  forms.ValidationError("Phone number already exists")
        return phonenumber

#     def clean_password2(self):
#         password = self.cleaned_data.get('password')

#         if  password != password:
#             raise forms.ValidationError("Password don't match")

#         return password
    
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            fullname=self.cleaned_data['fullname'],
            phonenumber=self.cleaned_data['phonenumber'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            register_as=self.cleaned_data['register_as'],
        )
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'photo',
            'fullname',
            'usertitle',
            'about',
            'city',
            'zip',
            'state',
            'facebook_link',
            'twitter_link',
            'google_link',
            'linkdin',
            'email',
            'address',
        ]

class Changepasswordform(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # comfirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')

    

