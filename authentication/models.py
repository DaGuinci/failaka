import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Supprime le champ username
    email = models.EmailField(unique=True)  # Utilise email comme identifiant unique

    USERNAME_FIELD = 'email'  # Définit email comme champ principal
    REQUIRED_FIELDS = []  # Aucun champ supplémentaire requis

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    thumbnail = models.ImageField(upload_to='users/', blank=True, null=True)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.groups.count() > 1:
            # Si l'utilisateur appartient à plusieurs groupes, ne garder que le dernier ajouté
            last_group = self.groups.last()
            self.groups.set([last_group])


