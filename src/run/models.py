from django.db import models
from route.models import Route
from vessel.models import Vessel

# Create your models here.
class Run(models.Model):
    vessel_name = models.ForeignKey(Vessel, on_delete=models.SET_NULL,related_name='+',null=True)
    source = models.CharField(max_length=20, null=True)
    destination = models.CharField(max_length=20, null=True)
    Mon = models.BooleanField(default=False)
    Tue = models.BooleanField(default=False)
    Wed = models.BooleanField(default=False)
    Thu = models.BooleanField(default=False)
    Fri = models.BooleanField(default=False)
    Sat = models.BooleanField(default=False)
    Sun = models.BooleanField(default=False)
