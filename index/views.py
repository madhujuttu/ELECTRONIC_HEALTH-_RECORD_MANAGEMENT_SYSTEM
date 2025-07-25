from django.shortcuts import render,redirect
from .models import patient, doctor

# Create your views here.

def index(request):
    return render(request,'index.html')

def change_password(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            return render(request,'forgetPassword.html',{'error' : 'New Password should be different'})
        else:
            try:
                #update password
                d = doctor.objects.get(Id = username)
                d.password = password2
                d.save()
                return redirect('doctorDashboard')
            except doctor.DoesNotExist:
                return render(request, 'forgetPassword.html', {'error': 'Doctor ID not found'})
            
    return render(request, 'forgetPassword.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user_type= request.POST['user']
        if username and password and user_type:
            if user_type == 'patient':
                try:
                    #retrive
                    p = patient.objects.get(username = username, password = password)
                    request.session['patient_id'] = p.Id
                    request.session['patient_name'] = p.fname + ' ' + p.lname
                    name = p.username;
                    if p.password == password:
                        return redirect('patientDashboard')
                    else:
                        return render(request,'Login.html',{'error' : 'Invalid password'})
                except patient.DoesNotExist:
                    return render(request,'Login.html',{'error' : 'USER doesnot exists please signup'})
            elif user_type == 'doctor':
                try:
                    d = doctor.objects.get(username = username, password = password)
                    request.session['doctor_id'] = d.Id
                    request.session['doctor_name'] = d.fname + ' ' + d.lname
                    if d.password == 'defaultpass':
                        return redirect('change_password')
                    return redirect('doctorDashboard')
                except doctor.DoesNotExist:
                    return render(request,'Login.html',{'error' : 'Invalid Patient credentials'})
            elif user_type == 'select':
                return render(request,'Login.html',{'error' : 'Invalid Patient credentials'})
    else:
        return render(request,'Login.html')
    
def logout(request):
    request.session.flush() 
    return redirect('index')

def signup(request):
    if request.method == 'POST':
        # Extract data from the POST request
        print('Form submitted')
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        patient_id = request.POST['patientId']
        aadhar = request.POST['aadhar']
        if patient.objects.filter(username = username).exists():
            return render(request, 'signup.html',{'error':'username is already exists'})
        elif patient.objects.filter(aadhar = aadhar).exists():
            return render(request, 'signup.html',{'error':'Aadhar number is already exists'})
        else:
            print(f"Firstname : {fname},Lastname : {lname},Username: {username}, Email: {email}, Aadhaar: {aadhar}, Patient ID: {patient_id}")
            # Create a new user instance and save it to the database
            user = patient(fname = fname,lname = lname,username=username, email=email, password=password, Id=patient_id, aadhar=aadhar)
            user.save()
            print('User created')
            return redirect('login')
    else:
        return render(request, 'signup.html')
    
    
def forgetPassword(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        user_type= request.POST['user']
        
       
        if password == password2:
            return render(request,'Login_forgetPassword.html',{'error' : 'Password must different from current password'})
        if username and password2 and password and user_type:
            if user_type == 'patient':
                try:
                    #retrive
                    p = patient.objects.get(username = username, password = password)
                    p.password = password2
                    p.save()
                    return redirect('patientDashboard')
                except patient.DoesNotExist:
                    return render(request,'Login_forgetPassword.html',{'error' : 'User not found'})
            elif user_type == 'doctor':
                try:
                    d = doctor.objects.get(username = username, password = password)
                    request.session['doctor_id'] = d.Id
                    request.session['doctor_name'] = d.fname + ' ' + d.lname
                    d.password = password2
                    d.save()
                    return redirect('doctorDashboard')
                except doctor.DoesNotExist:
                    return render(request,'Login_forgetPassword.html',{'error' : 'User not found'})
            elif user_type == 'select':
                return render(request,'Login_forgetPassword.html',{'error' : 'select either Doctor or Patient'})
    return render(request, 'Login_forgetPassword.html');

def get_all_patients(request):
    all_patients = patient.objects.all()
    return render(request, 'patients.html', {'patients': all_patients})
