from os import name
from django.urls import path
from real import views
from acc_user.views import *
from acc_user.views  import ResetPasswordView
from django.contrib.auth import views as auth_views


app_name = "index"

urlpatterns = [
    path('', views.homeview, name="home"),
    path('about/', views.AboutView, name="about-us"),
    path('add_property/', views.AddProperity, name="property"),
    path('search/', views.search, name='search'),
    path('property/<slug:slug>/', views.DetailsViews, name='property_details'),
    path('feature/<slug:slug>/', views.FeatureDetails, name='property_detai'),
    path('property_List', views.ProperityView, name='propertyview'),
    path('404', views.Error404 , name="404"),
    path('faq', views.Faq , name="faq"),
    path('blog', views.blogview , name="blog"),
    path('blogdetails/<slug:slug>/', views.postdetailview , name="blog_details"),
    path('contact', views.Contactview , name="contact"),
    path('property/edit/<slug>', views.EditView, name='edit'),
    path('featured/', views.FeatureView , name='featured'),
    path('bookmarklist/<slug>/', bookmark , name="add_book_list"),
    # path('plusbooklist/<slug>/', booklist_increment , name="plusbooklist"),
    # path('minubooklist/<slug>/', booklist_decrement , name="removebooklist"),
    path('deletebooklist/<slug>/', booklist_delete , name="deletebooklist"),


    # login and register
    path('change/',  changepassword.as_view() , name='change_password'),
    path('password_success/',  change_success, name="password_success"),
    path('signup/',  RegisterView, name="register"),
    path('login/',  LoginView, name="login"),
    path('agents/<int:slug>',  agentview, name="add_agent"),
    path('agentpage',  agentdashboard, name="agent_page"),
    path('logout/',  logout_View, name="logout"),
    path('dashboard/',  dashboardview, name="dashborad"),
    path('del/<slug>/',  views.del_listing, name="delete"),
    path('profile/', Myprofileview, name="myprofile"),
    path('myproperty/', mypropertyView, name="my_property"),
    path('booklist/', bookmarklistview, name="booklist"),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
     path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),     
]



