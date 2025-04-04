import uuid

from django.db import models

# from authentication.models import User

class Resource(models.Model):
        # UUID: UUID
        # author: User
        # name: String
        # description: String
        # thumbnail: image

    class Meta:
        abstract = True

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey('authentication.User', on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=150, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='resources/', blank=True, null=True)
    