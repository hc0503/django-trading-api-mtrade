# django imports
from django.test import TestCase, RequestFactory
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
import logging

# local imports
from mtrade.domain.users.models import UserPersonalData, UserBasePermissions
from mtrade.application.users.services import UserAppServices
from .views import infoLogger

class DebugLoggerTest(TestCase):
	def test_logging(self):
		with self.assertLogs('foo', level='DEBUG') as cm:
			logging.getLogger('foo').info('The info message')
			logging.getLogger('foo').error('The error message')
			logging.getLogger('foo').debug('The debug message')
			logging.getLogger('foo').warning('The warning message')
			logging.getLogger('foo').fatal('The fatal message')
		self.assertEqual(cm.output, [
			'INFO:foo:The info message',
			'ERROR:foo:The error message',
			'DEBUG:foo:The debug message',
			'WARNING:foo:The warning message',
			'FATAL:foo:The fatal message',
		])

class LoggerViewTest(APITestCase):
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
		response = infoLogger(request)
		self.assertIs(response.status_code, 200)