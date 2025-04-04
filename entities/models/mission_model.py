import uuid

from django.db import models

from entities.models.resource_model import Resource
from entities.models import (
    Site,
    Subsite,
)

class Mission(Resource):
    # notables: Notables-manyToMany
    # mission_members: String
    # type: String
    # period: String
    # biblio: String
    # citation: String


    # notables = models.ManyToManyField('Notable', blank=True, null=True)
    mission_members = models.CharField(max_length=150, blank=True, null=True)
    type = models.CharField(max_length=150, blank=True, null=True)
    period = models.CharField(max_length=150, blank=True, null=True)
    biblio = models.TextField(blank=True, null=True)
    citation = models.TextField(blank=True, null=True)