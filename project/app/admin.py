from django.contrib import admin
from .models import Profile,Group,Task,ChatQuestion,Message
# Register your models here.
admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(Task)
admin.site.register(ChatQuestion)
admin.site.register(Message)