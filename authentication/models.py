import uuid

from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class User(AbstractUser):
    username = None  # Supprime le champ username
    email = models.EmailField(unique=True)  # Utilise email comme identifiant unique

    USERNAME_FIELD = 'email'  # Définit email comme champ principal
    REQUIRED_FIELDS = []  # Aucun champ supplémentaire requis

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    thumbnail = models.ImageField(upload_to='users/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.groups.count() > 1:
            # Si l'utilisateur appartient à plusieurs groupes, ne garder que le dernier ajouté
            last_group = self.groups.last()
            self.groups.set([last_group])


