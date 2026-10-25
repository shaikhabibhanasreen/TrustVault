
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = "ADMIN"
    ROLE_OWNER = "OWNER"
    ROLE_VIEWER = "VIEWER"

    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_OWNER, "Owner"),
        (ROLE_VIEWER, "Viewer"),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_VIEWER,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"