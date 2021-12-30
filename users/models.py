from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class GolfUser(AbstractUser):

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    email = models.EmailField(_("email address"), unique=True)
    friends = models.ManyToManyField(
        "self",
        through="friend.Friendship",
        through_fields=("user", "friend"),
        related_name="+",
    )

    objects = UserManager()

    def __str__(self):
        return self.email
