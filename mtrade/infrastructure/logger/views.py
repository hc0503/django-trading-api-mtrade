# django import
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def infoLogger(request):
	"""
	API endpoint that tests info logger to be exported JSON log.
	"""

	try:
		logger.info('The info logger is called successfully.', extra={'referral_code': '52d6ce'})
	except Exception as e:
		raise APIException(e)

	return Response({
		'message': 'Logger info testing: check the log.json file in logs folder.'
	})
