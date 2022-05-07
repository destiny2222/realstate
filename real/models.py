from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
# Create your models here.

# user = get_user_model()

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=50, default='')
    # first_name = models.CharField(max_length=50, default='')
    register_as = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=20,unique=True)
    phonenumber = models.CharField(max_length=15, default='', blank=True, null=True)

    def _str_(self):
        return self.username


class Property(models.Model):
    property_title = models.CharField(max_length=225)
    status = models.CharField(max_length=225)
    property_type = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=10 ,decimal_places=2)
    area = models.CharField(max_length=225)
    bedrooms = models.CharField(max_length=225)
    bathrooms = models.CharField(max_length=225)
    bathrooms = models.CharField(max_length=225)
    image = models.FileField()
    address = models.CharField(max_length=225)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    description = RichTextField()
    building_Age = models.CharField(max_length=225 ,blank=True, null=True)
    garage = models.CharField(max_length=225 ,blank=True, null=True)
    Rooms = models.CharField(max_length=225 ,blank=True, null=True)

    def __str__(self):
        return self.property_title

class  Other_Feature(models.Model):
       property = models.ForeignKey(Property, on_delete=models.CASCADE)
       name = models.CharField(max_length=100)


class  Contact_Information(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=225)
    phone = models.CharField(max_length=100, blank=True , null=True)

                

