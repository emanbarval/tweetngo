from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    username = models.CharField(max_length=150, unique=True, verbose_name='Username')

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following')

class FollowerRequest(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_requests')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target_user_requests')
    is_accepted = models.BooleanField(default=False)
