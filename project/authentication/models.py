from django.db import models

from django.conf import settings
from django.db.models import query
from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import LANGUAGE_SESSION_KEY
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)