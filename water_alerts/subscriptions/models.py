from django.db import models
from django.contrib.auth import get_user_model
from geo.models import Region

User = get_user_model()

class UserSubscription(models.Model):
    CHANNEL_CHOICES = [
        ('SMS', 'SMS Text Message'),
        ('EMAIL', 'Email'),
        ('PUSH', 'Mobile Push'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='water_subscriptions')
    regions = models.ManyToManyField(Region)
    alert_types = models.JSONField(default=list)  # Store which alert types user wants
    channels = models.JSONField(default=list)  # Preferred notification channels
    language = models.CharField(max_length=10, default='en')
    verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = "User Water Alert Subscription"
        verbose_name_plural = "User Water Alert Subscriptions"
    
    def __str__(self):
        return f"{self.user} subscription"