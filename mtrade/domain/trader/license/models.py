from django.db import models

from lib.django import custom_models

class TraderLicense(custom_models.DatedModel):
    """
    Represents a Trader License.
    """
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=250)
