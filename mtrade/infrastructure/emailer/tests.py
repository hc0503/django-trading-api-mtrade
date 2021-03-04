# import django
from django.core import mail
from django.test import TestCase

class EmailTest(TestCase):
	def test_send(self):
		mail.send_mail('subject', 'body.', 'no-reply@mtrade.mx', ['no-reply@mtrade.mx'])
		assert len(mail.outbox) == 1
