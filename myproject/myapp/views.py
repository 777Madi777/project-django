from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta, date
from .models import Appointment, User, Doctor
from .forms import CustomUserCreationForm, ProfileForm, DoctorApplicationForm
from .utils import generate_time_slots
from django.contrib.auth import login


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user)  
            return redirect('profile')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    doctor = Doctor.objects.filter(user=request.user).first()
    return render(request, 'profile.html', {
        'user': request.user,
        'doctor': doctor
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def doctor_apply(request):
    user = request.user

    if user.is_doctor:
        return redirect('profile')

    if request.method == 'POST':
        form = DoctorApplicationForm(request.POST)
        if form.is_valid():
            if not hasattr(user, 'doctor'):
                Doctor.objects.create(
                    user=user,
                    specialty=form.cleaned_data['specialty']
                )
            return redirect('profile') 
    else:
        form = DoctorApplicationForm()

    return render(request, 'doctor_apply.html', {'form': form})

@login_required
def doctor_list(request):
    doctors = User.objects.filter(is_doctor=True)
    return render(request, 'doctor_list.html', {'doctors': doctors})

from django.utils.timezone import is_naive, make_aware

@login_required
def book_appointment(request, doctor_id):
    doctor_user = get_object_or_404(User, id=doctor_id, is_doctor=True)
    doctor = get_object_or_404(Doctor, user=doctor_user)
    
    today = date.today()
    next_week = today + timedelta(days=7)

    all_slots = generate_time_slots(today, next_week)

    booked_slots = Appointment.objects.filter(
        doctor=doctor, 
        date__range=(today, next_week)
    ).values_list('date', flat=True)

    available_slots = [slot for slot in all_slots if slot not in booked_slots]

    if request.method == 'POST':
        selected_slot = request.POST.get('slot')
        if selected_slot:
            dt = datetime.fromisoformat(selected_slot)
            if is_naive(dt):
                dt = make_aware(dt)
            Appointment.objects.create(
                doctor=doctor,
                patient=request.user,
                date=dt
            )
            return redirect('profile')

    return render(request, 'book_appointment.html', {
        'doctor': doctor,
        'available_slots': available_slots
    })

@login_required
def profile(request):
    user = request.user
    today = timezone.now().date()

    user_appointments = Appointment.objects.filter(patient=user,date__gte=today).order_by('date')

    doctor_appointments_today = []
    if user.is_doctor:
        doctor_appointments_today = Appointment.objects.filter(doctor__user=user,date__date=today
        ).select_related('patient').order_by('date')

    return render(request, 'profile.html', {
        'user_appointments': user_appointments,
        'doctor_appointments_today': doctor_appointments_today,
    })
