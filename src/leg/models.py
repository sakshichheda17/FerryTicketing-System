from django.db import models

# Create your models here.
class Leg(models.Model):
    date = models.DateField()
    run_id = models.PositiveSmallIntegerField()
    # route_id = models.PositiveSmallIntegerField()
    source = models.CharField(max_length=20, null=True)
    destination = models.CharField(max_length=20, null=True)
    vessel_name = models.CharField(max_length=20, null=True)
    departure_time = models.TimeField(null=True)
    arrival_time = models.TimeField(null=True)
    PASS = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    PARS = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    PCSS = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    PCRS = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    max_seats = models.PositiveIntegerField(null=True)
    cancelled_status =models.BooleanField(default=False,null=True)