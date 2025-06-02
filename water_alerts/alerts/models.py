from django.db import models
from django.contrib.gis.db import models as gis_models
from geo.models import Region

class Alert(models.Model):
    SEVERITY_LEVELS = [
        (1, 'Low - Notice'),
        (2, 'Moderate - Advisory'),
        (3, 'High - Warning'),
        (4, 'Critical - Emergency'),
    ]
    
    ALERT_TYPES = [
        ('OUTAGE', 'Water Outage'),
        ('CONTAMINATION', 'Water Contamination'),
        ('PRESSURE', 'Low Pressure'),
        ('MAINTENANCE', 'Planned Maintenance'),
    ]
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.IntegerField(choices=SEVERITY_LEVELS)
    title = models.CharField(max_length=120)
    description = models.TextField()
    affected_regions = models.ManyToManyField(Region)
    effective_from = models.DateTimeField()
    effective_to = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Spatial extent for map visualization
    affected_area = gis_models.GeometryField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['is_active', 'effective_from', 'effective_to']),
        ]
    
    def __str__(self):
        return f"{self.get_alert_type_display()}: {self.title}"