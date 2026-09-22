from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        unique=True
    )

    class Role(models.TextChoices):

        CUSTOMER = "customer", "Customer"

        STAFF = "staff", "Staff"

        MANAGER = "manager", "Manager"

        ADMIN = "admin", "Administrator"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    def __str__(self):
        return self.username