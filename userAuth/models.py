from django.db import models
from django.contrib.auth.models import User as MainUser

# Create your models here.

class userInfo(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    genders = (('male', 'male'), ('female', 'female'), ('other', 'other'))

    phone = models.CharField(max_length=15)
    gender = models.TextField(choices=genders)
    proPic = models.ImageField(blank=True, upload_to='propic')


    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + ' (' + self.user.username + ')'



