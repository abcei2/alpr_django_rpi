from django.db import models
from django.contrib.postgres.fields import ArrayField


class LPRCamera(models.Model):
    detection_zone = ArrayField(
        models.PositiveIntegerField(),size=4)

    url = models.URLField(unique=True)
    # Always use the format 'lon.gitude,lat.itude'
    geopoint = models.CharField(max_length=100)
    

class LPRCamera_allowed_plates(models.Model):

    allowed_plate= models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)
# Create your models here.

class LPRCamera_reports(models.Model):
    detected_plate=models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
