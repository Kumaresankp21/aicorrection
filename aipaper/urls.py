from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('register/', views.register, name='register'),
    path('create_exam/', views.create_exam, name='create_exam'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('student_info/', views.student_info, name='student_info'), 
]
