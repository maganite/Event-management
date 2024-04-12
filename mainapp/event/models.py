from django.db import models


class Eventdata(models.Model):
    id = models.IntegerField(primary_key=True)
    event_name = models.CharField(max_length=64)
    city_name = models.CharField(max_length=64)
    date = models.DateField()
    latitude =  models.CharField(max_length=32)
    longitude = models.CharField(max_length=32)