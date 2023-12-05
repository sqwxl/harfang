from django.db import models, transaction
import logging

logger = logging.getLogger(__name__)


class PointsMixin(models.Model):
    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=models.Q(points__gte=0),
                name="%(app_label)s_%(class)s_points_gte_0",
            )
        ]

    points = models.IntegerField(default=0)

    def increment_points(self):
        obj = type(self).objects.select_for_update().get(pk=self.pk)
        with transaction.atomic():
            obj.points += 1
            obj.save()

    def decrement_points(self):
        logger.debug("decrementing points")
        obj = type(self).objects.select_for_update().get(pk=self.pk)
        with transaction.atomic():
            if obj.points > 0:
                obj.points -= 1
                obj.save()
