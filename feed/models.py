from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User

# Create your models here.

class videoInfo(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = EmbedVideoField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title


class catagory(models.Model):
    title = models.CharField(max_length=30)
    descriotion = models.TextField(blank=True)

    def __str__(self):
        return self.title


class videoAndCategory(models.Model):
    video = models.ForeignKey('videoInfo', on_delete=models.CASCADE)
    catagory = models.ForeignKey('catagory', on_delete=models.CASCADE)



class comments(models.Model):
    video = models.ForeignKey('videoInfo', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()




