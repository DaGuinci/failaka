import uuid

from django.db import models

from entities.models.resource_model import Resource
from entities.models import Item

class Comment(Resource):
    # Item: Item
    # status: Enum

    class Status(models.TextChoices):
        PENDING = 'pending'
        VALIDATED = 'validated'
        REJECTED = 'rejected'
        DELETED = 'deleted'
    
    item= models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    status = models.CharField(max_length=9, choices=Status.choices, default=Status.PENDING)

