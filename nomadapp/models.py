from django.db import models

from django.conf import settings

# Create your models here.
class Adventure(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,)
    name = models.CharField(max_length=32)
    advType = models.IntegerField()
    advStatus = models.IntegerField()
