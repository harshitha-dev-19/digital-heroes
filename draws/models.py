from django.db import models
from django.contrib.auth.models import User

class Draw(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('simulated', 'Simulated'),
        ('published', 'Published'),
    ]
    month = models.DateField()  # store as first day of month
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    winning_numbers = models.JSONField(null=True, blank=True)  # list of 5 numbers
    jackpot_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Draw - {self.month}"

class Winner(models.Model):
    MATCH_CHOICES = [
        ('5', '5-Number Match'),
        ('4', '4-Number Match'),
        ('3', '3-Number Match'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]
    draw = models.ForeignKey(Draw, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match_type = models.CharField(max_length=1, choices=MATCH_CHOICES)
    prize_amount = models.DecimalField(max_digits=10, decimal_places=2)
    proof_image = models.ImageField(upload_to='proofs/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.user.username} - {self.match_type} match"