# django import
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services import EmailerServices
from rest_framework.exceptions import APIException

@api_view(['GET'])
def sendEmail(request):
	"""
	API endpoint that tests Emailer module with test SendGrid template id(d-59254528bee54e53852235bc6f769a46).
	"""
	emailer = EmailerServices()
	try:
		emailer.send('d-59254528bee54e53852235bc6f769a46', {
				'title': 'Test',
				'name': 'Devdreamsolution'
			},
			'no-reply@mtrade.mx',
			['no-reply@mtrade.mx'],
			'no-reply@mtrade.mx'
		)
	except Exception as e:
		raise APIException(e)

	return Response({
		'message': 'Emailer testing successfully: check the inbox.'
	})
