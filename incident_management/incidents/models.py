from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):
    SEVERITY_CHOICE = [
        ('Critical','Critical'),
        ('High','High'),
        ('Medium','Medium'),
        ('Low','Low'),
    ]

    STATUS_CHOICE = [
        ('New','New'),
        ('In Progress','In Progress'),
        ('Needs Review','Needs Review'),
        ('Needs Assistance','Needs Assistance'),
        ('Resolved','Resolved'),
        ('Closed','Closed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICE, default='Low')
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_incidents')
    external_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"
