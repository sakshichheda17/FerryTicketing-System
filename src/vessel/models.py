from django.db import models

# Create your models here.
class Vessel(models.Model):
    vessel_name = models.CharField(max_length=30)
    def __str__(self):
        return self.vessel_name