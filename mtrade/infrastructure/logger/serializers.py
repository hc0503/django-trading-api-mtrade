# django import
from rest_framework import serializers

# local import
from .models import Logger

class LoggerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Logger
		fields = [
			'id', 'level', 'module', 'short_description', 'raw_message', 'created_at'
		]