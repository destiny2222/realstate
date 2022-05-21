from django.urls import path
from .views import *
from acc_user.views import *
from acc_user.views  import ResetPasswordView
from django.contrib.auth import views as auth_views


app_name = "index"

urlpatterns = [
    path('', homeview, name="home"),
    path('about/', homeview, name="about-us"),
    path('add_property/', AddProperity, name="property"),
    path('search/', search, name='search'),
    path('property/<slug:slug>/', DetailsViews, name='property_details'),
    path('property_List', ProperityView, name='propertyview'),
    path('404', Error404 , name="404"),


    path('bookmarklist/<slug>/', bookmark, name="add_book_list"),
    # path('plusbooklist/<slug>/', booklist_increment , name="plusbooklist"),
    # path('minubooklist/<slug>/', booklist_decrement , name="removebooklist"),
    path('deletebooklist/<slug>/', booklist_delete , name="deletebooklist"),


    # login and register
    path('change/', changepassword.as_view() , name='change_password'),
    path('password_success/', change_success, name="password_success"),
    path('signup/', RegisterView, name="register"),
    path('login/', LoginView, name="login"),
    path('logout/', logout_View, name="logout"),
    path('dashboard/', dashboardview, name="dashborad"),
    path('profile/',Myprofileview, name="myprofile"),
    path('myproperty/',mypropertyView, name="my_property"),
    path('booklist/',bookmarklistview, name="booklist"),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
     path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),     
]



