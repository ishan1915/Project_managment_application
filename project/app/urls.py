from django.urls import path
from .views import signup_view,dashboard_view,profile_edit
urlpatterns=[
    path('signup/',signup_view,name='signup'),
    path('dashboard/',dashboard_view,name='dashboard'),
    path('profile_edit/',profile_edit,name='profile_edit'),
]