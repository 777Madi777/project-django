from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta, date
from .models import Appointment, User, Doctor
from .forms import CustomUserCreationForm, ProfileForm, DoctorApplicationForm
from .utils import generate_time_slots
from django.contrib.auth import login

# Главная страница
def home(request):
    return render(request, 'home.html')

# Регистрация пользователя
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

# Профиль пользователя
@login_required
def profile(request):
    doctor = Doctor.objects.filter(user=request.user).first()
    return render(request, 'profile.html', {
        'user': request.user,
        'doctor': doctor
    })

# Редактирование профиля пользователя
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

# Подача заявки на статус доктора
@login_required
def doctor_apply(request):
    if request.user.is_doctor:
        return redirect('profile')  

    if request.method == 'POST':
        form = DoctorApplicationForm(request.POST)
        if form.is_valid():
            user = request.user
            user.is_doctor = True 
            user.is_patient = False
            user.save()

            Doctor.objects.create(
                user=user,
                specialty=form.cleaned_data['specialty'],
                available_days=form.cleaned_data['available_days']
            )
            return redirect('profile') 
    else:
        form = DoctorApplicationForm()

    return render(request, 'doctor_apply.html', {'form': form})

# Список докторов
@login_required
def doctor_list(request):
    doctors = User.objects.filter(is_doctor=True)
    return render(request, 'doctor_list.html', {'doctors': doctors})

# Запись на прием
@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(User, id=doctor_id, is_doctor=True)
    today = date.today()
    next_week = today + timedelta(days=7)

    # Генерация всех возможных временных слотов на неделю
    all_slots = generate_time_slots(today, next_week)
    
    # Проверка занятых слотов
    booked_slots = Appointment.objects.filter(doctor=doctor, date__range=(today, next_week)).values_list('date', flat=True)
    available_slots = [slot for slot in all_slots if slot not in booked_slots]

    if request.method == 'POST':
        selected_slot = request.POST.get('slot')
        if selected_slot:
            # Преобразуем строку в datetime
            slot_dt = timezone.make_aware(datetime.fromisoformat(selected_slot))
            
            # Создаем запись о записи на прием
            Appointment.objects.create(
                doctor=doctor,
                patient=request.user,
                date=slot_dt
            )
            return redirect('profile')

    return render(request, 'book_appointment.html', {
        'doctor': doctor,
        'available_slots': available_slots
    })
