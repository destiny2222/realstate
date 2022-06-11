from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django_countries.fields import CountryField
from django.db.models.signals import pre_save
from django.utils import timezone
from datetime import datetime
# Create your models here.

# user = get_user_model()
  


class CustomUser(AbstractUser):
    package_plan = (
        ('BASIC PACKAGE', 'BASIC PACKAGE'),
        ('PLATINUM PACKAGE', 'PLATINUM PACKAGE'),
        ('STANDARD PACKAGE', 'STANDARD PACKAGE'),
    )
    
    fullname = models.CharField(max_length=50, default='')
    usertitle = models.CharField(max_length=50, default='')
    about = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    # register_as = models.CharField( max_length=100, default='')
    username = models.CharField(max_length=20,unique=True)
    phonenumber = models.CharField(max_length=15, default='', blank=True, null=True)
    facebook_link = models.CharField(max_length=50)
    twitter_link = models.CharField(max_length=200)
    google_link = models.CharField(max_length=200)
    linkdin = models.CharField(max_length=200)
    photo = models.FileField(default='avatar.png', upload_to='images/profile_img')
    address = models.TextField()
    package=models.CharField(choices=package_plan, default='BASIC PACKAGE', max_length=100)
    created = models.DateTimeField(auto_now_add=True , null=True, blank=True)


    def _str_(self):
        return self.username


class Agent(models.Model):
    user_agent = models.OneToOneField(CustomUser, related_name='agent', on_delete=models.CASCADE)
    Designation = models.CharField(max_length=50)
    landline = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    country = CountryField(multiple=False)
    is_approve = models.BooleanField(default=False)



        
    def __str__(self):
        return self.user_agent.fullname




class Listing(models.Model):
    listing_user = models.ForeignKey(CustomUser, related_name='listing_user' ,on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    status = models.CharField(max_length=225)
    property_type = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=10 ,decimal_places=2)
    area = models.CharField(max_length=225)
    bedrooms = models.CharField(max_length=225)
    bathrooms = models.CharField(max_length=225)
    address = models.CharField(max_length=225)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    description = models.TextField()
    building_Age = models.CharField(max_length=225 ,blank=True, null=True)
    garage = models.CharField(default=0,max_length=225 ,blank=True, null=True)
    Rooms = models.CharField(max_length=225 ,blank=True, null=True)
    sqft = models.CharField(max_length=225)
    # lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    image = models.FileField(upload_to='images/photos')
    photo_1 = models.ImageField(upload_to='images/photos', blank=True, null=True)
    photo_2 = models.ImageField(upload_to='images/photos', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='images/photos', blank=True, null=True)
    contact_name = models.CharField(max_length=100)
    contact_email = models.CharField(max_length=225)
    contact_phone = models.CharField(max_length=100, blank=True , null=True, unique=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(default='', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Listing, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("index:property_details", kwargs={'slug': self.slug})
    

class Review(models.Model):
    review = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=200)
    property_title = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.name    




class Bookmarklisting(models.Model):
    users = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    property = models.OneToOneField(Listing, on_delete=models.SET_NULL, null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.users.username


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=20)
    body = RichTextField()
    image = models.FileField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default='', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title


class Featured(models.Model):
    # feature = models.ForeignKey('self', related_name='feature_count', on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    status = models.CharField(max_length=225)
    property_type = models.CharField(max_length=225)
    price = models.FloatField()
    area = models.CharField(max_length=225)
    bedrooms = models.CharField(max_length=225)
    bathrooms = models.CharField(max_length=225)
    location = models.CharField(max_length=225)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    description = models.TextField()
    building_Age = models.CharField(max_length=225 ,blank=True, null=True)
    garage = models.CharField(default=0,max_length=225 ,blank=True, null=True)
    Rooms = models.CharField(max_length=225 ,blank=True, null=True)
    sqft = models.CharField(max_length=225)
    # lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    image = models.FileField(upload_to='images/photos')
    photo_1 = models.ImageField(upload_to='images/photos', blank=True, null=True)
    photo_2 = models.ImageField(upload_to='images/photos', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='images/photos', blank=True, null=True)
    contact_name = models.CharField(max_length=100)
    contact_email = models.CharField(max_length=225)
    contact_phone = models.CharField(max_length=100, blank=True , null=True, unique=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(default='', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Featured, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()        
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name
