# django import
from django.urls import path

# local imports
from .views import EmailVerification

urlpatterns = [
	path('users/<uidb64>/<token>/email-verification', EmailVerification.activate)
]
