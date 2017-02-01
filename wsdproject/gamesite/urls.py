from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

from . import views

urlpatterns = [
    url(r"^$", views.index, name='index'),
    url(r"^register$", login_forbidden(views.register), name='register'),
    url(r"^activate/(?P<key>.+)$", views.activation, name='activation'),
    url(r"^new-activation-link/(?P<username>\w+)/$", views.new_activation_link, name='new_activation_link'),
    url(r"^kirjaudu$", views.my_view),
    url(r"^thanks/", views.thanks, name='thanks'),
    url(r"^example_game$", views.example_game, name='example_game')
]
