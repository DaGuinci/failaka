import uuid

from django.db import models

from authentication.models import User

from entities.models.resource_model import Resource

class Subsite(Resource):

    # - site: Site
    # - location: Tuple(Float)
    # - chrono: Tuple(Datetime)
    # - justification: String
    # - settle_type: String (Enum?)
    # - material: String(Enum)
    # - remains: String

    site = models.ForeignKey('Site', on_delete=models.CASCADE, blank=False, null=False)
    location = models.JSONField(blank=True, null=True)
    chrono = models.JSONField(blank=True, null=True)
    justification = models.TextField(blank=True, null=True)
    settle_type = models.CharField(max_length=150, blank=True, null=True)
    material = models.CharField(max_length=150, blank=True, null=True)
    remains = models.TextField(blank=True, null=True)