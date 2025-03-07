import uuid

from django.db import models

from authentication.models import User

class Site(models.Model):
        # UUID: UUID
        # author: User
        # name: String
        # type: String (enum?)
        # description: String
        # subsites: Subsite
        # keywords: Dict
        # chrono: Tuple(Datetime)
        # location: Tuple(Float)
        # altitude: Float
        # location_name: String
        # geology: String
        # geo_description: String
        # historio: String
        # missions: Mission
        # justification: String

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey('authentication.User', on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=150, blank=False, null=False)
    type = models.CharField(max_length=150, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    # subsites = models.ForeignKey('Subsite', on_delete=models.CASCADE, blank=True, null=True)
    keywords = models.JSONField(blank=True, null=True)
    chrono = models.JSONField(blank=True, null=True)
    location = models.JSONField(blank=True, null=True)
    # altitude = models.FloatField(blank=True, null=True)
    location_name = models.CharField(max_length=150, blank=True, null=True)
    geology = models.CharField(max_length=150, blank=True, null=True)
    geo_description = models.TextField(blank=True, null=True)
    historio = models.TextField(blank=True, null=True)
    # missions = models.ForeignKey('Mission', on_delete=models.CASCADE, blank=True, null=True)
    justification = models.TextField(blank=True, null=True)