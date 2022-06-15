from django import forms
from django.contrib.auth import  get_user_model,authenticate,login
from django.contrib.auth.forms import PasswordChangeForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.core.validators import validate_email
from real.models import *
User = get_user_model()

register_plan = [
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
                raise forms.ValidationError("Username or Password not correct")
            if  not user:
                raise forms.ValidationError("This user does not exist")        
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(Loginform, self).clean(*args, **kwargs) 



class Signupform(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder': 'Full Name',}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'email','placeholder': 'Email',}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder': 'Username',}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'password','placeholder': '*******',}))
    confirm_password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'password','placeholder': 'Confirm password',}))
    # phonenumber = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text','placeholder': '123 546 5847',}))

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
    
    # def clean_number(self):
    #     phonenumber = self.cleaned_data['phonenumber'].lower()
    #     r = User.objects.filter(phonenumber=phonenumber)
    #     if r.count():
    #         raise  forms.ValidationError("phone number already exists")
    #     return phonenumber

    def clean_confirm_password(self):
        pas = self.cleaned_data['password']
        cpas = self.cleaned_data['confirm_password']
        MIN_LENGTH = 8
        if pas and cpas:
            if pas != cpas:
                raise forms.ValidationError("password and confirm password not match")
            else:
                if len(pas) < MIN_LENGTH:
                    raise forms.ValidationError("Password should have atleast %d characters " %MIN_LENGTH)
                if pas.isdigit():
                    raise forms.ValidationError("Password should not be all numeric")            

#     def clean_password2(self):
#         password = self.cleaned_data.get('password')

#         if  password != password:
#             raise forms.ValidationError("Password don't match")

#         return password
    
    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            fullname=self.cleaned_data['fullname'],
            # phonenumber=self.cleaned_data['phonenumber'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
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

class VerifyAgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ( 'Designation', 'description',
            'country',  'landline',
        )
    landline = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'text',
    }))
    Designation = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'type':'text',
        'placeholder': 'Designation',
    }))
    description = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
    }))
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class':'form-control',
            'id': 'country',
            'name': 'country',
        }))
    
    # def __init__(self, *args):
    #     super(agentform, self).__init__(*args)
        
# class Edit_Listing(forms.ModelForm):
#     class Meta:
#         model = Listing
#         fields = {'title', 'price', 'status', 'property_type', 'area', 'bedrooms', 'bathrooms', 'address',
#              'city', 'state', 'zipcode', 'description', 'building_Age', 'garage', 'Rooms', 'sqft',
#              'image', 'photo_1', 'photo_2', 'photo_3', 'contact_name', 'contact_email',
#              'contact_phone',
#         }
#     title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     price = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     status = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     area = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     city = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     contact_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     contact_phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     contact_email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','type':'email',}))
#     # image = forms.CharField(widget=forms.FileInput(attrs={'class':'form-control',}))
#     # photo_1 = forms.CharField(widget=forms.FileInput(attrs={'class':'form-control',}))
#     # photo_2 = forms.CharField(widget=forms.FileInput(attrs={'class':'form-control',}))
#     # photo_3 = forms.CharField(widget=forms.FileInput(attrs={'class':'form-control',}))
#     sqft = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     Rooms = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     garage = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control',}))
#     state = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     zipcode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     building_Age = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     bedrooms = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     bathrooms = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))
#     property_type = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text',}))    