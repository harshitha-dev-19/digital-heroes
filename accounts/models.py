from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    selected_charity = models.ForeignKey(
        'charities.Charity', 
        on_delete=models.SET_NULL, 
        null=True, blank=True
    )
    charity_percentage = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return self.user.username