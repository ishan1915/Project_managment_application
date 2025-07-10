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