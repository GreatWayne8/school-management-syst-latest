# models.py
from django.db import models
from django.conf import settings

class MedicalRecord(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE)
    record_date = models.DateField()
    condition = models.CharField(max_length=255)
    treatment = models.TextField()
    notes = models.TextField()
    doctor = models.CharField(max_length=255)
    doctors_phone_number = models.CharField(max_length=15)
    hospital = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.student.user.username} - {self.record_date}"
