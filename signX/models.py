from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Address(models.Model):
    """Model to store address information"""
    line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.line1}, {self.city}, {self.state} - {self.pincode}"


class Patient(models.Model):
    """Model to store patient profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    profile_picture = models.ImageField(upload_to='patient_profiles/', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    user_type = models.CharField(max_length=10, default='patient', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"Patient: {self.user.get_full_name() or self.user.username}"


class Doctor(models.Model):
    """Model to store doctor profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    profile_picture = models.ImageField(upload_to='doctor_profiles/', null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    user_type = models.CharField(max_length=10, default='doctor', editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Doctors"

    def __str__(self):
        return f"Doctor: {self.user.get_full_name() or self.user.username}"
