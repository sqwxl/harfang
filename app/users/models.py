from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from app.common.mixins import PointsMixin


class User(PointsMixin, AbstractUser):
    @property
    def is_moderator(self):
        return self.groups.filter(name="Moderator").exists()

    def __str__(self):
        return self.username


class Profile(models.Model):
    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.CharField(
        _("bio"), blank=True, max_length=settings.BIO_MAX_LENGTH
    )

    def __str__(self):
        return f"{self.user}'s profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
