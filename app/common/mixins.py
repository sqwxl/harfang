from django.db import models


class PointsMixin(models.Model):
    class Meta:
        abstract = True

    points = models.IntegerField(default=0)

    def increment_points(self):
        self.points = models.F("points") + 1
        self.save(update_fields=["points"])

    def decrement_points(self):
        # TODO prevent negative points? (shouldnt be possible)
        self.points = models.F("points") - 1
        self.save(update_fields=["points"])
