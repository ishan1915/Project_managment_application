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
     path('create_group/',create_group_view,name='create_group'),
     path('assign_task/',assign_task_view,name='assign_task'),

     path('get-group-members/<int:group_id>/', get_group_members, name='get_group_members'),


     path('update-task/<int:task_id>/',update_task_view,name='update-task'),

     path('group/<int:group_id>/', group_detail_view, name='group_detail'),

     path('group/<int:group_id>/add-member/', add_member_view, name='add_group_member'),


]