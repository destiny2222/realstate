from django.contrib import admin
from .models import  *
# class ListingAdmin(admin.ModelAdmin):
#     	exclude = ['slug']
# Register your models here.


# class  Other_Feature(admin.TabularInline):
#     model = Other_Feature 
    
# class  Contact_Information(admin.TabularInline):
#     model = Contact_Information

# class  Property_admin(admin.ModelAdmin):
#     inlines = (Other_Feature, Contact_Information)      


admin.site.register(CustomUser) 
admin.site.register(Listing)   
admin.site.register(Bookmarklisting)      
# admin.site.register(Contact_Information)      
     