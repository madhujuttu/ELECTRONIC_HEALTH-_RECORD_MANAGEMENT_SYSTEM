from django.shortcuts import render,redirect
from index.models import patient,doctor,PatientInformation
from .models import records,appointment
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import patient_login_required,doctor_login_required
@patient_login_required
def patientDashboard(request):
    print(f"Session data: {request.session.items()}")
    if 'patient_id' not in request.session:
        return redirect('login') 
    pid = request.session.get('patient_id')
    pname = request.session.get('patient_name')

    if not pid:  
        return redirect('login')
    
    try:
        patient_info = PatientInformation.objects.get(patient_id_id = pid)
    except PatientInformation.DoesNotExist:
        patient_info = None
    
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        date = request.POST['dob']
        gender = request.POST['gender']
        
        phone_number = request.POST['phonenum']
        email = request.POST['email']
        
        street = request.POST['street']
        city = request.POST['town']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']
        
        emergency_contact_name = request.POST['emergency_contact']
        emergency_phone_number = request.POST['emergency_pnum']
        
        medical_history = request.POST['medical_history']
        current_medications = request.POST['current_medications']
        allergies = request.POST['allergies']
        chronic_conditions = request.POST['chronic_conditions']
        
        height = request.POST['height']
        weight = request.POST['weight']
        bmi = request.POST['bmi']
        blood_type = request.POST['blood_type']
        
        covid_status = request.POST['covid_vaccination_status']
        flu_status = request.POST['flu_vaccination_status']
        
        primary_care_physician = request.POST['primary_care_physician']
        specialist = request.POST['specialist']
        
        if patient_info:
            patient_info.fname = fname
            patient_info.lname = lname
            patient_info.dob = date
            patient_info.gender = gender
            patient_info.phone_number = phone_number
            patient_info.email = email
            patient_info.street_address = street
            patient_info.city = city
            patient_info.state = state
            patient_info.postal_code = pincode
            patient_info.country = country
            patient_info.emergency_contact_name = emergency_contact_name
            patient_info.emergency_contact_phone = emergency_phone_number
            patient_info.medical_history = medical_history
            patient_info.current_medications = current_medications
            patient_info.allergies = allergies
            patient_info.chronic_conditions = chronic_conditions
            patient_info.height = height
            patient_info.weight = weight
            patient_info.bmi = bmi
            patient_info.blood_type = blood_type
            patient_info.covid_vaccination_status = covid_status
            patient_info.flu_vaccination_status = flu_status
            patient_info.primary_care_physician = primary_care_physician
            patient_info.specialist = specialist
            patient_info.save()
        else:
            # Create a new record
            patient_info = PatientInformation(
                fname=fname,
                lname=lname,
                dob=date,
                gender=gender,
                phone_number=phone_number,
                email=email,
                street_address=street,
                city=city,
                state=state,
                postal_code=pincode,
                country=country,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_phone=emergency_phone_number,
                medical_history=medical_history,
                current_medications=current_medications,
                allergies=allergies,
                chronic_conditions=chronic_conditions,
                height=height,
                weight=weight,
                bmi=bmi,
                blood_type=blood_type,
                covid_vaccination_status=covid_status,
                flu_vaccination_status=flu_status,
                primary_care_physician=primary_care_physician,
                specialist=specialist,
                patient_id_id=pid  
            )
            patient_info.save()
    d = doctor.objects.all()
    appointment_object = appointment.objects.filter(pid_id = pid)
    
    
    records_object = records.objects.filter(pid_id=pid)

    return render(request,'patient_interface.html',{'pid':pid,'pname':pname,
                                                    'patient_info':patient_info,'doctors':d,
                                                    'records': records_object,
                                                    'appointments': appointment_object
                                                    })
@doctor_login_required
def doctorDashboard(request):
    did = request.session.get('doctor_id')
    dname = request.session.get('doctor_name')
    appointment_object = appointment.objects.filter(did_id = did)
    
    accept = reject = pending = 0
    for i in appointment_object:
        if i.status == 'pending..':
            pending += 1
        elif i.status == 'accepted':
            accept += 1
        else:
            reject +=1
    return render(request,'doctor_interface.html',{'did':did,'dname':dname,'appointments': appointment_object,'accept':accept,'reject':reject,'pending':pending})

def records_view(request):
    pid = request.session.get('patient_id')
    if not pid:
        return redirect('login')  # Ensure the patient is logged in


    if request.method == 'POST':
        doctor_id = request.POST['doctorId']
        appointment_date = request.POST['appointmentDate']
        condition = request.POST['condition']
        medical_advice = request.POST['medicalAdvice']
        medications = request.POST['medications']

        # Debugging output
        print(f'Doctor ID: {doctor_id}, Appointment Date: {appointment_date}, Condition: {condition}, Medical Advice: {medical_advice}, Medications: {medications}')  
        
        if doctor_id and appointment_date and condition and medical_advice and medications:
            try:
                # Check if doctor exists
                doctor_instance = doctor.objects.get(Id=doctor_id)  
                
                # Create a new record
                record = records(
                    did_id=doctor_instance.Id, 
                    pid_id=pid,
                    doa=appointment_date,
                    condition=condition,
                    medical_advice=medical_advice,
                    medications=medications
                )
                record.save()
                print('Record saved successfully') 
                
                return redirect('patientDashboard')
                
            except doctor.DoesNotExist:
                return HttpResponse('Doctor ID does not exist', status=400)
    
    return render(request, 'patient_interface.html')

def appointment_view(request):
    pid = request.session.get('patient_id')
    if not pid:
        return redirect('login')
    
    if request.method == 'POST':
        did = request.POST.get('did')
        doa = request.POST.get('doa')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')
        appointmentId = request.POST.get('appointmentId')
        
        # Debugging output
        print(f"Received values - Doctor ID: {did}, Date of Appointment: {doa}, Mobile: {mobile}, Message: {message}, Appointment ID: {appointmentId}")  
        
        if doa and did and mobile and message and appointmentId :
            try:
                doctor_instance = doctor.objects.get(Id=did)  
                
                # Create a new record
                a = appointment(
                    did_id=doctor_instance.Id, 
                    pid_id = pid,
                    doa=doa,
                    mobile=mobile,
                    message=message,
                    aid=appointmentId
                )
                a.save()
                print('Appointment created successfully') 

                return redirect('patientDashboard')
                
            except doctor.DoesNotExist:
                return HttpResponse('Doctor ID does not exist', status=400)
        else:
            return HttpResponse('Invalid input: some fields are missing', status=400)

    return render(request, 'patient_interface.html')

def logout(request):
    request.session.flush()
    return redirect('index')

def records_view2(request):
    pid = request.session.get('patient_id')
    did = request.session.get('doctor_id')
    if not did:
        return redirect('login')  # Ensure the patient is logged in


    if request.method == 'POST':
        patient_id = request.POST['patientId']
        appointment_date = request.POST['appointmentDate']
        condition = request.POST['condition']
        medical_advice = request.POST['medicalAdvice']
        medications = request.POST['medications']

        # Debugging output
        print(f'Patient ID: {patient_id}, Appointment Date: {appointment_date}, Condition: {condition}, Medical Advice: {medical_advice}, Medications: {medications}')  
        
        if patient_id and appointment_date and condition and medical_advice and medications:
            try:
                # Check if doctor exists
                patient_instance = patient.objects.get(Id=patient_id)  
                
                # Create a new record
                record = records(
                    did_id=did, 
                    pid_id=patient_instance.Id,
                    doa=appointment_date,
                    condition=condition,
                    medical_advice=medical_advice,
                    medications=medications
                )
                record.save()
                print('Record saved successfully') 
                
                return redirect('doctorDashboard')
                
            except patient.DoesNotExist:
                return HttpResponse('patient ID does not exist', status=400)
    
    return render(request, 'doctor_interface.html')

def update_appointment_status(request, aid, status):
    if request.method == 'POST':
        app = appointment.objects.get(aid = aid)
        
        if status == 'accepted':
            app.status = 'accepted'
            
        elif status == 'rejected':
            app.status = 'rejected'
            
        app.save()

    return redirect('doctorDashboard')


def patient_forget_password(request):
    pid = request.session.get('patient_id')
    pat = patient.objects.get(Id = pid)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            return render(request,'patient_forget_password.html',{'error' : 'New Password should be different','pat':pat})
        else:
            try:
                #update password
                d = patient.objects.get(Id = username)
                d.password = password2
                d.save()
                return redirect('patientDashboard',)
            except patient.DoesNotExist:
                return render(request, 'patient_forget_password.html', {'error': 'patient ID not found'})
            
    return render(request, 'patient_forget_password.html',{'pat' : pat})

def doctor_forget_password(request):
    did = request.session.get('doctor_id')
    doc = doctor.objects.get(Id = did)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            return render(request,'patient_forget_password.html',{'error' : 'New Password should be different'})
        else:
            try:
                #update password
                d = doctor.objects.get(username = username)
                d.password = password2
                d.save()
                return redirect('doctorDashboard')
            except doctor.DoesNotExist:
                return render(request, 'patient_forget_password.html', {'error': 'patient ID not found'})
            
    return render(request, 'patient_forget_password.html',{'doc':doc})

# views.py
def delete_appointment(request, appointment_id):
    appointment = appointment.objects.get(aid=appointment_id)
    appointment.delete()


def delete_record(request):
    record = records.objects.get(Id = patient)
    record.delete()
    return render(request,'patientDashboard');
