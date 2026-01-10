from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = {
        "checking": "Checking",
        "analysis": "Analysis",
        "archived": "Archived",
        "failed": "Failed",
        "pending": "Pending",
        "success": "Success"
    }

    name = models.CharField(max_length=512)
    description = models.TextField(blank=True, default="")
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default="checking")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"{self.id} - {self.name}"
    
class Standard(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"

class StandardRule(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField(blank=True, default="")
    group = models.CharField(max_length=256)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"
