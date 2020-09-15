from django.db import models

# Create your models here.
class Route(models.Model):
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    class Meta(object):
        unique_together = [
            'source','destination'
        ]