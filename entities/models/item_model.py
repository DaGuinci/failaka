import uuid

from django.db import models

from entities.models.resource_model import Resource
from entities.models import (
    Site,
    Subsite,
)

class Item(Resource):
    # type: Enum
    # identification: String
    # site: Site
    # subsite: Site.subsite
    # thumbnail: Thumbnail
    # item_date: Tuple(Datetime)
    # family: String
    # scient_name: String
    # material: String (Enum?)
    # current_location: String
    # references: String
    # citation: String
    # method1(): ReturnType

    type = models.CharField(max_length=150, blank=False, null=False)
    identification = models.CharField(max_length=150, blank=True, null=True)
    site = models.ForeignKey('Site', on_delete=models.CASCADE, blank=True, null=True)
    subsite = models.ForeignKey('Subsite', on_delete=models.CASCADE, blank=True, null=True, related_name='subsite')
    # thumbnail = models.ImageField(upload_to='item_thumbnails/', blank=True, null=True)
    item_date = models.JSONField(blank=True, null=True)
    family = models.CharField(max_length=150, blank=True, null=True)
    scient_name = models.CharField(max_length=150, blank=True, null=True)
    material = models.CharField(max_length=150, blank=True, null=True)
    current_location = models.CharField(max_length=150, blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    citation = models.TextField(blank=True, null=True)