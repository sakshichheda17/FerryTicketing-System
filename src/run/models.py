from django.db import models
from route.models import Route
from vessel.models import Vessel

# Create your models here.
class Run(models.Model):
    vessel_name = models.ForeignKey(Vessel, on_delete=models.SET_NULL,related_name='+',null=True)
    source = models.CharField(max_length=20, null=True)
    destination = models.CharField(max_length=20, null=True)
    departure_time = models.TimeField(null=True)
    arrival_time = models.TimeField(null=True)
    PASS = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    PARS = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    PCSS = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    PCRS = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    max_seats = models.PositiveIntegerField(null=True)
    Mon = models.BooleanField(default=False)
    Tue = models.BooleanField(default=False)
    Wed = models.BooleanField(default=False)
    Thu = models.BooleanField(default=False)
    Fri = models.BooleanField(default=False)
    Sat = models.BooleanField(default=False)
    Sun = models.BooleanField(default=False)
