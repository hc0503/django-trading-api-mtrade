# django import
from django.test import TestCase
from django.core import mail
from rest_framework.test import APITestCase

# local import
from .services import Mail

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

		assert len(mail.outbox) == 1

class EmailerViewTest(APITestCase):
	def setUp(self):
		self.url = '/api/v0/emailers/send'
		self.status_code = 200

	def test_send_mail(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, self.status_code)
