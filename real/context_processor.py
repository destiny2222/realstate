from django.contrib.auth import get_user_model

User = get_user_model()

def user_count(request):
   return { 'total_user' : User.objects.all().count() }

#    <div>
#     {{ user_count }}
# </div>