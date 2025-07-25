from django.db import models
from index.models import patient,doctor
# Create your models here.

class records(models.Model):
    did = models.ForeignKey(doctor, on_delete=models.CASCADE)
    pid = models.ForeignKey(patient, on_delete=models.CASCADE)
    doa = models.DateField()
    condition = models.CharField(max_length=50)
    medical_advice = models.CharField(max_length=50)
    medications = models.CharField(max_length=50)
    
class appointment(models.Model):
    aid = models.CharField(max_length=10, primary_key=True)
    did = models.ForeignKey(doctor, on_delete=models.CASCADE)
    pid = models.ForeignKey(patient,on_delete= models.CASCADE)
    doa = models.DateField()
    mobile = models.BigIntegerField()
    message = models.CharField(max_length=100)
    status = models.CharField(default='pending..')