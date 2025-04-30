from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Doctor, Appointment

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_doctor', 'is_patient', 'is_staff', 'has_doctor_request')
    list_filter = ('is_doctor', 'is_patient', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()
    actions = ['approve_doctor', 'reject_doctor']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'gender', 'date_of_birth')}),
        ('Роли', {'fields': ('is_doctor', 'is_patient')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'gender', 'date_of_birth',
                       'is_doctor', 'is_patient', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    @admin.display(description='Заявка на доктора')
    def has_doctor_request(self, obj):
        return hasattr(obj, 'doctor') and not obj.is_doctor

    @admin.action(description="✅ Одобрить заявку на доктора")
    def approve_doctor(self, request, queryset):
        updated = 0
        for user in queryset:
            if hasattr(user, 'doctor') and not user.is_doctor:
                user.is_doctor = True
                user.save()
                updated += 1
        self.message_user(request, f"Одобрено заявок: {updated}")

    @admin.action(description="❌ Отклонить заявку на доктора")
    def reject_doctor(self, request, queryset):
        updated = 0
        for user in queryset:
            if hasattr(user, 'doctor') and not user.is_doctor:
                user.doctor.delete()
                updated += 1
        self.message_user(request, f"Отклонено заявок: {updated}")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty')
    search_fields = ('user__email', 'specialty')
    list_filter = ('specialty',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'date', 'time', 'is_confirmed')
    list_filter = ('doctor', 'patient', 'is_confirmed')
    search_fields = ('doctor__user__email', 'patient__email')

    @admin.display(description='Time')
    def time(self, obj):
        return obj.time
