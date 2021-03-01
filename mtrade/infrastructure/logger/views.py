# django import
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def testLogger(request):
	"""
	API endpoint that tests logger to be exported JSON log.
	"""

	logger.info('The index is called successfully.', extra={'referral_code': '52d6ce'})

	return Response({
		'message': 'Logger testing: check the log.json file in logs folder.'
	})
