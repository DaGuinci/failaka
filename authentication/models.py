import uuid

from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class User(AbstractUser):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.groups.count() > 1:
            # Si l'utilisateur appartient à plusieurs groupes, ne garder que le dernier ajouté
            last_group = self.groups.last()
            self.groups.set([last_group])

#   - UUID: UUID
#   - firstname: String
#   - lastname: String
#   - groupe: Group
#   - email: String
#   - password: String
#   - thumbnail: path

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (["password"])


    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=150, unique=True, blank=False, null=False)
    thumbnail = models.ImageField(upload_to='users/', blank=True, null=True)


