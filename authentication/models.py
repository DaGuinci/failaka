import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

#   - UUID: UUID
#   - firstname: String
#   - lastname: String
#   - role: Enum
#   - email: String
#   - password: String

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (["password"])

    class Role(models.TextChoices):
        ADMIN = 'admin'
        VALID = 'validator'
        NOROLE = 'norole'

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=150, unique=True, blank=False, null=False)
    role = models.CharField(max_length=9, choices=Role.choices, default=Role.NOROLE)
