from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Doctor, Appointment

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_doctor', 'is_patient', 'is_staff')
    list_filter = ('is_doctor', 'is_patient', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Роли', {'fields': ('is_doctor', 'is_patient')}),
    )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty')
    search_fields = ('user__email', 'specialty')  
    list_filter = ('specialty',)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'time', 'is_confirmed')  
    list_filter = ('doctor', 'patient', 'is_confirmed') 
    search_fields = ('doctor__username', 'patient__username')

    
    @admin.display(description='Time')
    def time(self, obj):
        return obj.time  

    # Если is_confirmed не добавлено в модель, убираем из list_display и list_filter
    # Если оно добавлено в модель, вот так его можно использовать:
    # def is_confirmed(self, obj):
    #    return obj.is_confirmed

admin.site.register(Appointment, AppointmentAdmin)


