from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.db.models.signals import pre_save
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
    register_as = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=20,unique=True)
    phonenumber = models.CharField(max_length=15, default='', blank=True, null=True)
    facebook_link = models.CharField(max_length=50)
    twitter_link = models.CharField(max_length=200)
    google_link = models.CharField(max_length=200)
    linkdin = models.CharField(max_length=200)
    photo = models.FileField(default='avatar.png', upload_to='images/profile_img')
    address = models.TextField()
    package=models.CharField(choices=package_plan, default='BASIC PACKAGE', max_length=100)


    def _str_(self):
        return self.username



class Listing(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
    image = models.FileField()
    photo_1 = models.ImageField(upload_to='images/photos', blank=True, null=True)
    photo_2 = models.ImageField(upload_to='images/photos', blank=True, null=True)
    photo_3 = models.ImageField(upload_to='images/photos', blank=True, null=True)
    photo_4 = models.ImageField(upload_to='images/photos', blank=True, null=True)
    photo_5 = models.ImageField(upload_to='images/photos', blank=True, null=True)
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
    
    # class Meta:
    #     db_table = "app_Listing"

# def create_slug(instance, new_slug=None):
#     slug = slugify(instance.title)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Listing.objects.filter(slug=slug).order_by('-id')
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" % (slug, qs.first().id)
#         return create_slug(instance, new_slug=new_slug)
#     return slug

# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)                     
# pre_save.connect(pre_save_post_receiver, Listing)



class Bookmarklisting(models.Model):
    users = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    property = models.OneToOneField(Listing, on_delete=models.SET_NULL, null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.users.username




