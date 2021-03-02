# django import
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def infoLogger(request):
	"""
	API endpoint that tests info logger to be exported JSON log.
	"""

	logger.info('The info logger is called successfully.', extra={'referral_code': '52d6ce'})

	return Response({
		'message': 'Logger info testing: check the log.json file in logs folder.'
	})
