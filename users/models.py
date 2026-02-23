# from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("PM", "Project Manager"),
        ("DEV", "Developer"),
        ("QA", "QA Tester"),
        ("MGR", "Manager"),
        ("AP", "Approver"),
        ("TL", "Test Lead"),
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    company_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
