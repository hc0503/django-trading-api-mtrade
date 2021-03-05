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
		'no-reply@mtrade.mx',
		['no-reply@mtrade.mx'],
		'd-59254528bee54e53852235bc6f769a46',
		{
			'title': 'testTitle',
			'name' : 'testName',
		},
		reply_to = 'no-reply@mtrade.mx',
	)
	
	try:
		mail.send()
	except Exception as e:
		raise APIException(e)

	return Response({
		'message': 'Emailer testing successfully: check the inbox.'
	})
