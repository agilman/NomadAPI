from django.db import models

from django.conf import settings

# Create your models here.
class Adventure(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,)
    name = models.CharField(max_length=32)
    advType = models.IntegerField()
    advStatus = models.IntegerField()

class Map(models.Model):
    adv = models.ForeignKey(Adventure,on_delete=models.CASCADE,related_name="maps")
    name = models.CharField(max_length=32)

class Segment(models.Model):
    map = models.ForeignKey(Map,on_delete=models.CASCADE, related_name="segments")
    startTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
    distance = models.IntegerField() #distance in meters

class WayPoint(models.Model):
    segment = models.ForeignKey(Segment,on_delete=models.CASCADE, related_name="coordinates")
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
