from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserRegistrationForm,AnswerSheetUploadForm,ExamCreationForm
from app.models import AnswerSheet


def home(request):
    return render(request, 'home.html')

def user_login(request):
    role = request.GET.get('role')  # Get role from URL query param

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if role == user.profile.role:  # Check role matches
                login(request, user)
                if role == 'student':
                    return redirect('student_dashboard')
                else:
                    return redirect('teacher_dashboard')
            else:
                messages.error(request, f"You are not registered as a {role}.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html', {'role': role})


@login_required
def student_dashboard(request):
    return render(request,"student/student_dashboard.html")

@login_required
def teacher_dashboard(request):
    return render(request,"teacher/teacher_dashboard.html")

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Assign role to Profile
            role = form.cleaned_data['role']
            user.profile.role = role
            user.profile.save()

            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register/register.html', {'form': form})


@login_required
def student_dashboard(request):
    student = request.user

    if request.method == 'POST':
        form = AnswerSheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            answer_sheet = form.save(commit=False)
            answer_sheet.student = student
            answer_sheet.save()
            return redirect('student_dashboard')
    else:
        form = AnswerSheetUploadForm()

    uploaded_sheets = AnswerSheet.objects.filter(student=student)

    return render(request, 'student_dashboard/student_dashboard.html', {
        'form': form,
        'uploaded_sheets': uploaded_sheets
    })


def create_exam(request):
    if request.method == 'POST':
        form = ExamCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle form data and save files here
            exam_type = form.cleaned_data['exam_type']
            year = form.cleaned_data['year']
            subject = form.cleaned_data['subject']
            staff_name = form.cleaned_data['staff_name']
            question_paper = form.cleaned_data['question_paper']
            answer_key = form.cleaned_data['answer_key']

            # TODO: Save the files and exam details to the database

            messages.success(request, "Exam created and files uploaded successfully!")
            return redirect('teacher_dashboard')  # Redirect to dashboard after success
    else:
        form = ExamCreationForm()

    return render(request, 'teacher/create_exam.html', {'form': form})

def student_info(request):
    return HttpResponse("Working on it")