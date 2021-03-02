# django import
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# local import
from .models import Logger
from .serializers import LoggerSerializer

class LoggerViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows loggers to be viewed or edited
	"""
	queryset = Logger.objects.all().order_by('created_at')
	serializer_class = LoggerSerializer
