from django.db import models
from django import forms
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='profile') #1 to 1 link with Django User
	activation_key = models.CharField(max_length=40)
	key_expires = models.DateTimeField()


class Game(models.Model):
	developer = models.ForeignKey(User, related_name='developer')
	title = models.CharField(max_length=225, blank=True)
	game_url = models.URLField(default="")
	price = models.IntegerField(default=15)
	image_url = models.URLField(default="")
	websiteURL = models.CharField(max_length=225, blank=True)
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


class Payment(models.Model):
	#payment = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
	pid = models.CharField(max_length=225, blank=True)
	price = models.IntegerField()
	ref =  models.IntegerField(null=True)
	checksum = models.CharField(max_length=225, blank=True)
	result = models.CharField(max_length=20)
	date = models.DateTimeField()

	def __str__(self):
		return self.pid + ',' + str(self.price) + ',{}'.format(self.ref)

class Save(models.Model):
	game = models.ForeignKey(Game, related_name="saves")
	user = models.ForeignKey(User, default=0, related_name='player')
	gamestate = models.TextField(max_length=200, blank=True, null=True)
	#points = models.FloatField(null=True, blank=True)
