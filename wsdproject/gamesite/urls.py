from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

from . import views

urlpatterns = [
    url(r"^$", views.index, name='index'),
    url(r"^register$", login_forbidden(views.register), name='register'),
    url(r"^activate/(?P<key>.+)$", views.activation, name='activation'),
    url(r"^new-activation-link/(?P<username>\w+)/$", views.new_activation_link, name='new_activation_link'),
    url(r"^account/$", views.my_view, name='myview'),
    url(r"^thanks/", views.thanks, name='thanks'),
	url(r"^gameshop$", views.gameshop, name='gameshop'),
	url(r'^gameshop/(?P<id>[0-9]+)/$', views.game_detail, name='detail'),

	url(r'^gameshop/(?P<id>[0-9]+)/payment$', views.payment, name='payment'),
	url(r'^payment/success$', views.paymentsuccess, name='payment success'),
	url(r'^payment/payment_cancel$$', views.paymentcancel, name='payment cancel'),
	url(r'^payment/payment_error$', views.paymenterror, name='payment error'),
    url(r'^gamesave/$', views.save, name='save'),

    url(r'^game/(?P<gametitle>\w+)/$', views.gameview, name='gameview'),
    url(r'^game/(?P<gametitle>\w+)/edit/$', views.editgame, name='editgame'),
    url(r'^game/(?P<gametitle>\w+)/delete/$', views.deletegame, name='deletegame'),
    url(r"^addgame$", views.addgame, name='addgame'),
    url(r"^addgame/success$", views.gameview, name='addgame success'),
    url(r"^submitscore$", views.submit_score, name='submit_score'),
]
