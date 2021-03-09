# django import
from django.test import TestCase
from django.core import mail
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory

# local import
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices
from .services import Mail
from .views import sendEmail

class EmailerServiceTest(TestCase):
	def test_send(self):
		mailer = Mail(
			'This is the subject',
			from_email = 'no-reply@mtrade.mx',
			to = ['no-reply@mtrade.mx'],
			bcc = ['bcc@mtrade.mx'],
		)
		mailer.template_id = 'd-59254528bee54e53852235bc6f769a46'
		mailer.dynamic_template_data = {
			'title': 'testTitle',
			'name': 'testName'
		}
		mailer.send()

		self.assertEqual(len(mail.outbox), 1)

class EmailerViewTest(APITestCase):
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

	def test_send_mail(self):
		request = self.factory.get('/api/v0/emailers/send')
		force_authenticate(request, user=self.user_01)
		response = sendEmail(request)
		self.assertIs(response.status_code, 200)
