# django import
import uuid
from django.db import models

class Logger(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	level = models.CharField(max_length=100)
	module = models.CharField(max_length=100)
	short_description = models.CharField(max_length=100)
	raw_message = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'loggers'