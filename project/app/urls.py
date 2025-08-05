from django.urls import path
from .views import *
from . import views

urlpatterns=[
path('api/signup/', views.SignupAPI.as_view(), name='api-signup'),
    path('api/login/', views.LoginAPI.as_view(), name='api-login'),
    path('api/logout/', views.LogoutAPI.as_view(), name='api-logout'),

    
    path('api/dashboard/', views.DashboardAPI.as_view(), name='api-dashboard'),
    path('api/profile/', views.ProfileAPI.as_view(), name='api-profile'),

     path('api/adminlogin/',views.AdminLogin.as_view(),name='adminlogin'),
    path('api/admin-dashboard/', views.AdminDashboardAPI.as_view(), name='api-admin-dashboard'),

    
    path('api/groups/create/', views.CreateGroupAPI.as_view(), name='api-create-group'),
    path('api/mygroups/',views.MyGroupAPI.as_view(),name='mygroups'),
    path('api/groups/<int:group_id>/members/', views.GroupMembersAPI.as_view(), name='api-group-members'),
    path('api/groups/<int:group_id>/add-member/', views.AddGroupMemberAPI.as_view(), name='api-add-member'),
    path('api/groups/<int:group_id>/', views.GroupDetailAPI.as_view(), name='api-group-detail'),

     path('api/tasks/assign/', views.AssignTaskAPI.as_view(), name='api-assign-task'),
    path('api/tasks/<int:task_id>/update/', views.UpdateTaskAPI.as_view(), name='api-update-task'),
     
    path('api/marktaskcomplete/<int:task_id>/',views.MarkCompleteTask.as_view(),name='marktaskcomplete'),

    
    path('api/chat/users/', views.ChatListAPI.as_view(), name='api-chat-users'),
    path('api/chat/messages/<int:user_id>/', views.ChatMessagesAPI.as_view(), name='api-chat-messages'),
    path('api/chat/send/', views.SendMessageAPI.as_view(), name='api-send-message'),

















 
]