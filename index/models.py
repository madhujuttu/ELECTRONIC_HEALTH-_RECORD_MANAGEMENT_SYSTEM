from django.db import models

class patient(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    Id = models.CharField(max_length=10, primary_key=True)
    aadhar = models.BigIntegerField()
    
class Hospital(models.Model):
    hid = models.CharField(max_length=10,primary_key=True)
    hname = models.CharField(max_length=25)
    haddr = models.CharField(max_length=100)
    
class doctor(models.Model):
    hid = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    fname = models.CharField(max_length=50, blank=True, null=True)
    lname = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    Id = models.CharField(max_length=10, primary_key=True)
    aadhar = models.BigIntegerField(blank=True, null=True)
    specialization = models.CharField(max_length=40,default='')

class PatientInformation(models.Model):
    patient_id = models.ForeignKey(patient, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    # Address information
    street_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    # Emergency contact
    emergency_contact_name = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True, null=True)

    # Health information
    medical_history = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)

    # Health metrics
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Height in cm
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Weight in kg
    bmi = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    blood_type = models.CharField(max_length=3, blank=True, null=True)

    # Vaccination info
    covid_vaccination_status = models.CharField(max_length=20, blank=True, null=True)
    flu_vaccination_status = models.CharField(max_length=20, blank=True, null=True)

    # Doctor and specialist information
    primary_care_physician = models.CharField(max_length=50, blank=True, null=True)
    specialist = models.CharField(max_length=100, blank=True, null=True)

