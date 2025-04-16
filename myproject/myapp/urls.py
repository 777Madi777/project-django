from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('doctor-apply/', views.doctor_apply, name='doctor_apply'),
    path('profile/', views.profile, name='profile'), 
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:doctor_id>/book/', views.book_appointment, name='book_appointment'),

]
