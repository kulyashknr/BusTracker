from django.db import models


# Create your models here.
class Route(models.Model):
    start_station = models.CharField(max_length=255)
    end_station = models.CharField(max_length=255)


class Bus(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route')
    distance = models.FloatField()
    #time = models.CharField(max_length=100)



