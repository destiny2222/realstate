from django.urls import path
from .views import *
from acc_user.views import *

app_name = "index"

urlpatterns = [
    path('', homeview, name="home"),
    path('property', AddProperity, name="property"),
    # login and register
    path('signup', RegisterView, name="register"),
    path('login', LoginView, name="login"),
    path('logout', logout_View, name="logout"),
]