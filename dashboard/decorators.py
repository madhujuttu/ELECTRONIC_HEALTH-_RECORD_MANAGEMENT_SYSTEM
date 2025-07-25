from django.shortcuts import redirect

def patient_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        
        if 'patient_id' not in request.session:
            return redirect('login')  
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def doctor_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        
        if 'doctor_id' not in request.session:
            return redirect('login')  
        return view_func(request, *args, **kwargs)
    return _wrapped_view

