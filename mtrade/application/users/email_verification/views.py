# django import
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User

# local import
from .tokens import email_verification_token

class EmailVerification():
	@api_view(['POST'])
	def activate(request, uidb64, token):
		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except(TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None
		if user is not None and email_verification_token.check_token(user, token):
			user.is_active = True
			user.save()
			return Response({
				'message': 'Thank you for your email confirmation. Now you can login your account.'
			})
		else:
			return Response({
				'message': 'Activation link is invalid!'
			})
