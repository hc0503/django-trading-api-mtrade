# django import
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import Mail
from rest_framework.exceptions import APIException

@api_view(['GET'])
def sendEmail(request):
	"""
	API endpoint that tests Emailer module with test SendGrid template_id (d-59254528bee54e53852235bc6f769a46).
	"""
	mail = Mail(
		'testSubject',
		from_email = 'no-reply@mtrade.mx',
		to = ['no-reply@mtrade.mx', 'admin@mtrade.mx'],
		bcc = ['bcc@mtrade.mx'],
	)
	mail.template_id = 'd-59254528bee54e53852235bc6f769a46'
	mail.dynamic_template_data = {
		'title': 'testTitle',
		'name': 'testName'
	}
	
	try:
		mail.send()
	except Exception as e:
		raise APIException(e)

	return Response({
		'message': 'Emailer testing successfully: check the inbox.'
	})
