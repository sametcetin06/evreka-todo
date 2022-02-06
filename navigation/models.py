from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _


class Vehicle(models.Model):
    plate = models.CharField(max_length=256, unique=True, verbose_name="Plate")
    created_date = models.DateTimeField(default=timezone.now, verbose_name="Vehicle Created Date")
    active = models.BooleanField(default=True, verbose_name="Vehicle Active")


class NavigationRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now, verbose_name="Record Transaction Date")
    # If these fields are kept as PointFields instead of FloatFields, later calculations can be faster.
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")

    # If a record is wanted to be brought from the NavigationRecord table,
    # the index is created according to the vehicle_id and datetime, since the data size will be too large.
    class Meta:
        indexes = [
            models.Index(fields=['vehicle_id', '-datetime'])
        ]


# This model records the last navigation data of each vehicle.
# Thus, when we want to bring the last location data of all vehicles, it will come quickly.
# As an alternative to this table, it could be done with cache with redis.
# It was done this way because it was requested to use Django ORM.
class LastNavigationRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now, verbose_name="Record Transaction Date")
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")


# System Logs Model
class Log(models.Model):
    user_id = models.IntegerField(verbose_name='Kullanıcı', null=True, blank=True)
    action = models.CharField(max_length=64, db_index=True)
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(null=True)
    obj = GenericForeignKey("content_type", "object_id")
    data = JSONField(null=True, blank=True)
    extra = JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    request_url = models.CharField(blank=True, null=True, max_length=512)
    ip_address = models.GenericIPAddressField(_('User IP'), null=True, blank=True)
    request_method = models.CharField(_('http method'), blank=True, null=True, max_length=16)

    class Meta:
        ordering = ["-timestamp"]