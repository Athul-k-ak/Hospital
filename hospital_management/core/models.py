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
    registered_at = models.DateField()  # Changed to store the entered date
    last_visit = models.DateField(null=True, blank=True) 
    def __str__(self):
        return self.name

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()  # Storing consultation date
    time = models.TimeField(auto_now_add=True)  # Automatically capture the time

    def __str__(self):
        return f"{self.patient.name} - {self.date}"


class Staff(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

class CasualtyReport(models.Model):
    name = models.CharField(max_length=100, default='Unknown')   # Name of the casualty
    report = models.TextField()  # Casualty report
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Amount field
    report_date = models.DateField(default=timezone.now)  # Date field (date only, no time)

    def __str__(self):
        return f"{self.name} - {self.report_date}"
