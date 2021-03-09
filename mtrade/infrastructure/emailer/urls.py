# django import
from django.urls import path

# local imports
from . import views

urlpatterns = [
	path('emailers/send', views.sendEmail),
]
