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
    analyzed = models.BooleanField(null=False, default=False)
    analyzed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        standard_name = 'standard_not_found'
        if self.standard:
            standard_name = self.standard.name
        return f"{self.id} - {self.project.name} <> {standard_name}"

    def set_analysis_result(self):
        self.status = "approved"
        for validation_rule in self.validationrule_set.all():
            if validation_rule.fulfilled == False:
                self.status = "failed"
                break
        return self


class ValidationRule(models.Model):
    validation = models.ForeignKey(Validation, on_delete=models.CASCADE)
    standard_rule = models.ForeignKey(StandardRule, null=True, on_delete=models.SET_NULL)
    fulfilled = models.BooleanField(null=True, default=None)
    note = models.TextField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        standard_rule_name = 'standard_rule_not_found'
        if self.standard_rule:
            standard_rule_name = self.standard_rule.name
        return f"{self.id} - {self.validation.name}:{standard_rule_name}"


class Account(models.Model):
    SUBSCRIPTION_CHOICES = {
        "trial": "trial",
        "basic": "basic",
        "intermediate": "intermediate",
        "advanced": "advanced",
        "customized": "customized"
    }

    PAYMENT_STATUS_CHOICES = {
        "free": "free",
        "awaiting_payment": "awaiting_payment",
        "paid": "paid",
        "not_paid": "not_paid",
        "expired": "expired"
    }

    name = models.CharField(max_length=512)
    cnpj = models.CharField(max_length=512, null=True, default=None)
    email = models.CharField(max_length=512, null=True, default=None)
    phone = models.CharField(max_length=512, null=True, default=None)
    active = models.BooleanField(default=True)
    subscription = models.CharField(max_length=512, choices=SUBSCRIPTION_CHOICES, default="trial")
    payment_status = models.CharField(max_length=512, choices=PAYMENT_STATUS_CHOICES, default="free")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.name}"


class UserAccount(models.Model):
    ROLE_CHOICES = {
        "guest": "guest",
        "employee": "employee",
        "manager": "manager",
        "director": "director"
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    role = models.CharField(max_length=512, choices=ROLE_CHOICES, default="director")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.account.name}::{self.user.name}"


class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.project.name}::{self.user.name}"
