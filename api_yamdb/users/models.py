from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(r'^[\w.@+-]+')]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True)
    last_name = models.CharField(
        max_length=150,
        blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=150,
        default=UserRole.USER,
        choices=UserRole.choices,
    )

    @property
    def is_admin(self):
        return (
            self.role == UserRole.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_user(self):
        return self.role == UserRole.USER
