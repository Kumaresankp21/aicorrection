from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student_exam_fill/', views.student_exam_fill, name='student_exam_fill'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('register/', views.register, name='register'),
    path('create_exam/', views.create_exam, name='create_exam'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('exams/<int:exam_id>/submissions/', views.view_exam_submissions, name='view_exam_submissions'),
    path('students_info',views.student_info,name="students_info"),
    path('submission/<int:submission_id>/result/', views.view_result, name='view_result'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
