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
#   - created_date: Datetime

    class Role(models.TextChoices):
        ADMIN = 'admin'
        USER = 'user'

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=150, unique=True, blank=False, null=False)
    role = models.CharField(max_length=5, choices=Role.choices, default=Role.USER)
