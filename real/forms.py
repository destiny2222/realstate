from dataclasses import field
from charset_normalizer import models
from django import  forms
from .models import Property



class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'property_title':forms.TextInput(attrs={'class': 'form-control'}),
            'status':forms.TextInput(attrs={'class': 'form-control'}),
            'property_type':forms.Select(attrs={'class': 'form-control'}),
            'price':forms.Select(attrs={'class': 'form-control'}),
        }
