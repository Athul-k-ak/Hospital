from django.db import models
from django.utils import timezone

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    reg_id = models.CharField(max_length=10, unique=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()  # Remove auto_now_add=True
    time = models.TimeField()  # Remove auto_now_add=True
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Consultation for {self.patient.name}"


class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

class CasualtyReport(models.Model):
    report = models.TextField()
    report_date = models.DateTimeField(default=timezone.now)
