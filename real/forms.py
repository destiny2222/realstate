from django import  forms
from django.forms import ModelForm
from .models import *
from .choices import *




class PropertyFormAdmin(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'status':forms.Select(choices=status_choice,  attrs={'class': 'form-control', 'required': 'True'}),
            'property_type':forms.Select(choices=properity_type_choice, attrs={'class': 'form-control', 'required': 'True'}),
            'price':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'area':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'bedrooms':forms.Select(choices=bedrooms_choices,  attrs={'class': 'form-control', 'required': 'True'}),
            'bathrooms':forms.Select(choices=bath_rooms ,attrs={'class': 'form-control', 'required': 'True'}),
            'image':forms.FileInput(attrs={'class': ' pb-6'}),
            'photo_1':forms.FileInput(attrs={'class': ' pb-6'}),
            'photo_2':forms.FileInput(attrs={'class': ' pb-6'}),
            'photo_3':forms.FileInput(attrs={'class': ' pb-6'}),
            'address':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'city':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'state':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'zipcode':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'sqft':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'description':forms.Textarea(attrs={'class': 'form-control h-120 ', 'required': 'True'}),
            'building_Age':forms.Select(choices=build_age,  attrs={'class': 'form-control', 'required': 'True'}),
            'garage':forms.Select(choices=egarn, attrs={'class': 'form-control', 'required': 'True'}),
            'Rooms':forms.Select(choices=room, attrs={'class': 'form-control', 'required': 'True'}),
            'contact_name':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'contact_email':forms.EmailInput(attrs={'class': 'form-control', 'required': 'True'}),
            'contact_phone':forms.TextInput(attrs={'class': 'form-control'}),
        }


class PropertyForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title','status','property_type','price','area','bedrooms', 'bathrooms',
            'image','photo_1','photo_2','photo_3','address','city','state','zipcode',
            'sqft','description', 'building_Age','garage','Rooms','contact_name',
            'contact_email','contact_phone'
        ]
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'status':forms.Select(choices=status_choice,  attrs={'class': 'form-control', 'required': 'True'}),
            'property_type':forms.Select(choices=properity_type_choice, attrs={'class': 'form-control', 'required': 'True'}),
            'price':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'area':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'bedrooms':forms.Select(choices=bedrooms_choices,  attrs={'class': 'form-control', 'required': 'True'}),
            'bathrooms':forms.Select(choices=bath_rooms ,attrs={'class': 'form-control', 'required': 'True'}),
            'image':forms.FileInput(attrs={'class': ' pb-6'}),
            'photo_1':forms.FileInput(attrs={'class': ' pb-6'}),
            'photo_2':forms.FileInput(attrs={'class': ' pb-6'}),
            'photo_3':forms.FileInput(attrs={'class': ' pb-6'}),
            'address':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'city':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'state':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'zipcode':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'sqft':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'description':forms.Textarea(attrs={'class': 'form-control h-120 ', 'required': 'True'}),
            'building_Age':forms.Select(choices=build_age,  attrs={'class': 'form-control', 'required': 'True'}),
            'garage':forms.Select(choices=egarn, attrs={'class': 'form-control', 'required': 'True'}),
            'Rooms':forms.Select(choices=room, attrs={'class': 'form-control', 'required': 'True'}),
            'contact_name':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'contact_email':forms.EmailInput(attrs={'class': 'form-control', 'required': 'True'}),
            'contact_phone':forms.TextInput(attrs={'class': 'form-control'}),
        }


    # def clean(self):
    #     print(self.changed_data, 'yessss')
    #     cleaned_data = super().clean()
    #     user = self.cleaned_data.get('user')
    #     print(user ,'yed userr')
    #     package = user.package
    #     qs = Listing.objects.filter(user=user).count()
    #     print(user, package, qs)


    # def __init__(self, user=None, **kwargs):
    #     super(PropertyForm, self).__init__(**kwargs)
    #     if user is not None:
    #         self.fields['user'].queryset = CustomUser.objects.all()

 
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'  


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'message', 'property_title', 'email')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ht-80', 'placeholder':'Your Email'}),
            'property_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Property Title'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Messages'}),
        }
