from django.db import models
from django.utils import timezone


class Bin(models.Model):
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")
    created_date = models.DateTimeField(default=timezone.now)


class Operation(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="Operation Name")
    bin = models.ManyToManyField(Bin, related_name="bin", through="BinOperation")


# It was created to hold collection_frequency and last_collection data for each operation and bin pairs.
class BinOperation(models.Model):
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, verbose_name="Bin")
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name="Operation")
    collection_frequency = models.IntegerField(default=0, verbose_name="Collection Frequency")
    last_collection = models.DateTimeField(verbose_name="Last Collection Date")