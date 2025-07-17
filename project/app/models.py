from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    email=models.EmailField()
    phone=models.IntegerField(blank=True,null=True)
    address=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profle "
    

class Group(models.Model):
    name=models.CharField(max_length=100)
    members=models.ManyToManyField(User,related_name='user_groups')

    def __str__(self):
        return self.name
    


class Task(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    assigned_to=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    deadline=models.DateField()
    uploaded_file=models.FileField(upload_to='uploads/',blank=True,null=True)
    user_description=models.TextField(blank=True,null=True)
    is_completed=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.assigned_to.username}"
    



class ChatQuestion(models.Model):
    question=models.CharField(max_length=300)
    answer=models.TextField()
    link=models.URLField(blank=True,null=True)

    def __str__(self):
        return self.question