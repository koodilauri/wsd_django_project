from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from gamesite.models import Game

class UserForm(ModelForm):
	Password = forms.CharField(widget=forms.PasswordInput)
	Re_enter_Password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ['username', 'email']



class PaymentForm(forms.Form):
	amount = forms.CharField(label='Amount', max_length=100)
	pid = forms.CharField(label='Amount', max_length=100)
	sid = forms.CharField(label='Amount', max_length=100)
	checksum = forms.CharField(label='Amount', max_length=100)

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'game_url', 'price', 'image_url', 'websiteURL', 'sid', 'skey','genre']
