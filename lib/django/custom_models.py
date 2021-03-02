# python imports
from datetime import datetime
from dataclasses import dataclass

# django imports
from django.db import models

class DatedModel(models.Model):
    """
    A DatedModel includes fields that reflect when the model has been created
    or modified
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

@dataclass(frozen=True)
class ModelDates():
    created_at: datetime
    modified_at: datetime
