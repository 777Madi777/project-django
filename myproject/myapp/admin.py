from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Doctor, Appointment


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_doctor', 'is_patient', 'is_staff')
    list_filter = ('is_doctor', 'is_patient', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Роли', {'fields': ('is_doctor', 'is_patient')}),
    )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'available_days')
    search_fields = ('user__username', 'specialty')
    list_filter = ('specialty',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'is_confirmed')
    list_filter = ('is_confirmed', 'date', 'doctor')
    search_fields = ('patient__username', 'doctor__user__username')
    ordering = ('-date', 'time')
