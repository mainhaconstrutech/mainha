from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    STATUS_CHOICES = {
        "checking": "Checking",
        "analysis": "Analysis",
        "archived": "Archived",
        "failed": "Failed",
        "pending": "Pending",
        "approved": "Approved"
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
    group = models.CharField(max_length=256, blank=True, default="")
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Validation(models.Model):
    STATUS_CHOICES = {
        "analysis": "Analysis",
        "failed": "Failed",
        "pending": "Pending",
        "approved": "Approved"
    }

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    standard = models.ForeignKey(Standard, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default="analysis")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        standard_name = 'standard_not_found'
        if self.standard: standard_name = self.standard.name
        return f"{self.id} - {self.project.name} <> {standard_name}"
