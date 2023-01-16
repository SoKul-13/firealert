from django.db import models

# Create your models here. 
class IrwinData(models.Model):
    irwinid = models.CharField(max_length=50, unique=True)
    longitude = models.DecimalField(max_digits=19, decimal_places=15)
    lattitude = models.DecimalField(max_digits=19, decimal_places=15)   
    incidentname = models.CharField(max_length=256)
    city = models.CharField(max_length=30,null=True)
    county = models.CharField(max_length=30)
    state = models.CharField(max_length=3)
    cdate = models.DateTimeField()
    mdate = models.DateTimeField()

class ZipData(models.Model):
    zip = models.IntegerField(unique=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=3)
    longitude = models.DecimalField(max_digits=19, decimal_places=15)
    lattitude = models.DecimalField(max_digits=19, decimal_places=15)

class WeatherData(models.Model):
    windspeed = models.IntegerField(max_length=4)
    winddegree = models.IntegerField(max_length=4)
    