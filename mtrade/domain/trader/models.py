from django.db import models

from lib.django import custom_models

from .license.models import TraderLicense

class Trader(custom_models.DatedModel):
    """
    Represents a Trader
    """
    id = models.UUIDField(primary_key=True, editable=False)
    license = models.ForeignKey(TraderLicense, on_delete=models.SET_NULL, null=True)
    institution = models.UUIDField()
