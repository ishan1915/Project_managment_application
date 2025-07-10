from django.urls import path
from .views import *
urlpatterns=[
    path('signup/',signup_view,name='signup'),
    path('login/',user_login,name='user_login'),
    path('dashboard/',dashboard_view,name='dashboard'),
    path('profile_edit/',profile_edit,name='profile_edit'),

    path('logout/',custom_logout_view,name='logout'),

     path('admin-dashboard/',admin_dashboard,name='admin-dashboard'),
     path('admin_edit/',admin_edit,name='admin_edit'),
]