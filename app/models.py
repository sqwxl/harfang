from django.conf import settings
from django.db import models
from django.utils import timezone


class Vote(models.Model):
    class Meta:
        abstract = True
        indexes = [models.Index(fields=["user"])]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submit_date = models.DateTimeField(default=timezone.now, editable=False)
