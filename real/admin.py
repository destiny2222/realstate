from django.contrib import admin
from .models import  *

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'email', 'approved_comment')
    list_filter = ('approved_comment', 'created_date')
    search_fields = ('name', 'email', 'message')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved_comment=True)


class AgentAdmin(admin.ModelAdmin):
    list_display = ['user', 'country',  'is_approve']

# class  Other_Feature(admin.TabularInline):
#     model = Other_Feature 
    
# class  Contact_Information(admin.TabularInline):
#     model = Contact_Information

# class  Property_admin(admin.ModelAdmin):
#     inlines = (Other_Feature, Contact_Information)      


admin.site.register(CustomUser) 
admin.site.register(Listing)   
admin.site.register(Bookmarklisting)      
admin.site.register(Post)      
admin.site.register(Featured)      
admin.site.register(Agent, AgentAdmin)     