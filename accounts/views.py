from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserSignupForm

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            if user.is_patient:
                return redirect('patient_dashboard')
            elif user.is_doctor:
                return redirect('doctor_dashboard')
    else:
        form = UserSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def patient_dashboard(request):
    return render(request, 'accounts/patient_dashboard.html')

def doctor_dashboard(request):
    return render(request, 'accounts/doctor_dashboard.html')
