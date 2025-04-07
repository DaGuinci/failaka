import uuid

from django.db import models

from entities.models.resource_model import Resource
from entities.models import (
    Site,
    Subsite,
)

class Notable(Resource):
    # first_name: String
    # last_name: String


    # notables = models.ManyToManyField('Notable', blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)