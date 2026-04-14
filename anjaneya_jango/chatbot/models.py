from django.db import models


class Destination(models.Model):
    city = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    ratings = models.FloatField()
    distance = models.CharField()
    place_desc = models.TextField()

    def __str__(self):
        return f"{self.place} in {self.city}"
