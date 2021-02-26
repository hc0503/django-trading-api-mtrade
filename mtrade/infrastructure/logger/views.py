# django import
from django.http import HttpResponse
import logging

logger = logging.getLogger('mtrade_log')

def testLogger(request):
	logger.info('The index is called successfully.', extra={'referral_code': '52d6ce'})
	return HttpResponse("Hello logging test.")
