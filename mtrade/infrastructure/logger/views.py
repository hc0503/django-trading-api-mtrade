# django import
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def debugLogger(request):
	"""
	API endpoint that tests debug logger to be exported JSON log.
	"""

	logger.debug('The debug logger is called successfully.', extra={'referral_code': '56df7d'})

	return Response({
		'message': 'Logger debug testing: check the log.json file in logs folder.'
	})

@api_view(['GET'])
def infoLogger(request):
	"""
	API endpoint that tests info logger to be exported JSON log.
	"""

	logger.info('The info logger is called successfully.', extra={'referral_code': '52d6ce'})

	return Response({
		'message': 'Logger info testing: check the log.json file in logs folder.'
	})

@api_view(['GET'])
def warningLogger(request):
	"""
	API endpoint that tests warning logger to be exported JSON log.
	"""

	logger.warning('The warning logger is called successfully.', extra={'referral_code': '7s8fw5'})

	return Response({
		'message': 'Logger warning testing: check the log.json file in logs folder.'
	})

@api_view(['GET'])
def errorLogger(request):
	"""
	API endpoint that tests error logger to be exported JSON log.
	"""

	logger.error('The error logger is called successfully.', extra={'referral_code': '9s58fs'})

	return Response({
		'message': 'Logger error testing: check the log.json file in logs folder.'
	})

@api_view(['GET'])
def fatalLogger(request):
	"""
	API endpoint that tests fatal logger to be exported JSON log.
	"""

	logger.fatal('The fatal logger is called successfully.', extra={'referral_code': '62sdf4'})

	return Response({
		'message': 'Logger fatal testing: check the log.json file in logs folder.'
	})
