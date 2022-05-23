

from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    users_id = models.IntegerField()
    profile_picture = models.ImageField(upload_to = 'profile_pic', default = 'default.jpg')
    location = models.CharField(max_length=25, blank=True)
    bio = models.TextField(blank=True)


    def __str__(self):
        return self.user.username



class Post(models.Model):
    id = models.UUIDField(primary_key=True ,  default=uuid.uuid4)
    user = models.CharField(max_length=25)
    caption = models.TextField(blank=True)
    picture = models.ImageField(upload_to = 'post_pic')
    uploaded_date = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    

    def __str__(self):
        return self.user

class LikePost(models.Model):
    username = models.CharField(max_length=25)
    post_id= models.CharField(max_length=100)


    def __str__(self):
        return self.username



class FollowerCount(models.Model):
    follower = models.CharField(max_length=50)
    user = models.CharField(max_length=25)


    def __str__(self):
        return self.user

