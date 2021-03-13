# django import
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

# local import
from .tokens import email_verification_token
from mtrade.infrastructure.emailer.services import Mail
from mtrade.domain.users.models import User

class EmailVerification():
	@api_view(['POST'])
	@permission_classes([IsAuthenticated])
	def resend(request, uid):
		try:
			current_site = get_current_site(request)
			user = User.objects.get(pk=uid)
			mail = Mail(
				subject = 'Activate your account',
				from_email = settings.EMAIL_FROM_ADDRESS,
				to = [user.email],
				template_id = settings.SENDGRID_EMAIL_VERIFICATION_TEMPLATE_ID,
				dynamic_template_data = {
					'domain': current_site.domain,
					'uidb64': urlsafe_base64_encode(force_bytes(uid)),
					'token': email_verification_token.make_token(user)
				}
			)
			mail.send(fail_silently=False)
		except Exception as e:
			raise APIException(e)
		return Response({
			'message': 'Please confirm your mail box to verify your email address'
		})

	@api_view(['GET'])
	@permission_classes([IsAuthenticated])
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
