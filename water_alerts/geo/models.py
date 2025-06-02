from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Region(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)  # e.g. "P345-X"
    geometry = models.PolygonField(srid=4326)  # WGS84
    centroid = models.PointField(srid=4326)
    population = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['code']),
            models.GistIndex(fields=['geometry']),
            models.GistIndex(fields=['centroid']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class WaterInfrastructure(models.Model):
    INFRASTRUCTURE_TYPES = [
        ('RESERVOIR', 'Reservoir'),
        ('PUMP_STATION', 'Pump Station'),
        ('TREATMENT_PLANT', 'Treatment Plant'),
        ('MAIN_PIPE', 'Main Pipe'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=INFRASTRUCTURE_TYPES)
    location = models.PointField(srid=4326)
    regions_served = models.ManyToManyField(Region)
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"