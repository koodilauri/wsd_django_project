from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile') #1 to 1 link with Django User
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()


class Game(models.Model):
    title = models.CharField(max_length=225, blank=True)
    game_url = models.URLField(default="")
    price = models.IntegerField(default=15)
    image_url = models.URLField(default="")
    websiteURL = models.CharField(max_length=225, blank=True)
    sid = models.CharField(max_length=225, blank=True)
    skey = models.CharField(max_length=225, blank=True)
    genre = models.TextField(default="action")

    def __str__(self):
        return self.title + ' - ' + self.game_url

class ScoreBoard(models.Model):
    websiteURL = models.CharField(max_length=225, blank=True)
    score = models.IntegerField(default="")
    user = models.ForeignKey(User, default=0 , related_name='user')
    def __unicode__(self):
         return '%s  %s points' % (self.user, self.score)
    #def __str__(self):
    #    return self.websiteURL + ' - ' + self.score
