# django import
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# local import
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices
from .views import EmailVerification
from .tokens import email_verification_token

class EmailVerificationTest(APITestCase):
	def setUp(self):
		self.factory = APIRequestFactory()
		self.u_data_01 = UserPersonalData(
			username = 'Teser',
			first_name = 'Testerman',
			last_name = 'Testerson',
			email = "testerman@example.com"
		)
		self.u_permissions_01 = UserBasePermissions(
			is_staff = False,
			is_active = False
		)
		self.user_01 = UserAppServices.create_user(self.u_data_01, self.u_permissions_01)

	def test_resend(self):
		request = self.factory.post('/api/v0/users/resend-email-verification/%s' % (self.user_01.id))
		force_authenticate(request, user=self.user_01)
		response = EmailVerification.resend(request, self.user_01.id)
		self.assertIs(response.status_code, 200)

	def test_activate(self):
		uidb64 = urlsafe_base64_encode(force_bytes(self.user_01.id))
		token = email_verification_token.make_token(self.user_01)
		request = self.factory.get('/api/v0/users/email-verification/%s/%s' % (uidb64, token))
		response = EmailVerification.activate(request, uidb64, token)
		self.assertIs(response.status_code, 200)