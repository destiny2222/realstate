from django import  forms
from .models import *

bed_rooms = [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
    ]
bath_rooms = [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
    ]
egarn = [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
    ]
room = [
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
    ]
prop_type = [
            ('Houses', 'Houses'),
            ('Apartment', 'Apartment'),
            ('Villas', 'Villas'),
            ('Commercial', 'Commercial'),
            ('Offices', 'Offices'),
            ('Garage', 'Garage'),
    ]
build_age = [
            ('0 - 5 Years', '0 - 5 Years'),
            ('0 - 10 Years', '0 - 10 Years'),
            ('0 - 20 Years', '0 - 20 Years'),
            ('20+ Years', '20+ Years'),
    ]


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'property_title':forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'status':forms.TextInput(attrs={'class': 'form-control'}),
            'property_type':forms.Select(choices=prop_type, attrs={'class': 'form-control'}),
            'price':forms.TextInput(attrs={'class': 'form-control'}),
            'area':forms.TextInput(attrs={'class': 'form-control'}),
            'bedrooms':forms.Select(choices=bed_rooms,  attrs={'class': 'form-control'}),
            'bathrooms':forms.Select(choices=bath_rooms ,attrs={'class': 'form-control'}),
            'image':forms.FileInput(attrs={'class': 'form-control'}),
            'address':forms.TextInput(attrs={'class': 'form-control'}),
            'city':forms.TextInput(attrs={'class': 'form-control'}),
            'state':forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode':forms.TextInput(attrs={'class': 'form-control'}),
            'description':forms.Textarea(attrs={'class': 'form-control h-120 '}),
            'building_Age':forms.Select(choices=build_age,  attrs={'class': 'form-control'}),
            'garage':forms.Select(choices=egarn, attrs={'class': 'form-control'}),
            'Rooms':forms.Select(choices=room, attrs={'class': 'form-control'}),
            # 'name':forms.TextInput(attrs={'class': 'form-control'}),
            'contact_name':forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email':forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone':forms.EmailInput(attrs={'class': 'form-control'}),
        }
       