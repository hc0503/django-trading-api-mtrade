# django import
from django.test import TestCase
from django.core import mail

# local import
from .services import Mail


class MailTest(TestCase):
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
	