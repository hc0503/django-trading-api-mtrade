# django import
from django.urls import path

# local imports
from .views import EmailVerification

urlpatterns = [
	path('users/resend-email-verification/<uid>', EmailVerification.resend),
	path('users/email-verification/<uidb64>/<token>', EmailVerification.activate),
]
