from django.db import models


class PointsMixin(models.Model):
    class Meta:
        abstract = True

    points = models.IntegerField(default=0)

    def increment_points(self):
        self.points = models.F("points") + 1
        self.save(update_fields=["points"])

    def decrement_points(self):
        if self.points > 0:
            self.points = models.F("points") - 1
            self.save(update_fields=["points"])
