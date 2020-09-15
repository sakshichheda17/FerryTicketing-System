from django.db import models
from run.models import Run

# Create your models here.
class Ticket(models.Model):
    passenger_id = models.PositiveSmallIntegerField(null=True)
    source = models.CharField(max_length=20, null=True)
    destination = models.CharField(max_length=20, null=True)
    vessel_name = models.CharField(max_length=20, null=True)
    departure_time = models.TimeField(null=True)
    arrival_time = models.TimeField(null=True)
    no_of_adults = models.PositiveSmallIntegerField()
    no_of_children = models.PositiveSmallIntegerField()
    SINGLE = 'S'
    RETURN = 'R'
    choices = [
        (SINGLE, 'Single'),
        (RETURN, 'Return'),
    ]
    journey_type = models.CharField(max_length=1,choices=choices,default=SINGLE)
    leg_id = models.PositiveSmallIntegerField(null=True)
    booking_time = models.DateTimeField(null=True)
    journey_amount = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(null=True, max_digits=10, decimal_places=2)