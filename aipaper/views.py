from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserRegistrationForm,StudentExamForm,ExamForm
from app.models import StudentExam,Exam
from .ocr import generate_ocr
from .extract_question_answerkey import question_answer_content
from .preprocess_ocr import preprocess_ocr_question_wise
from .evalution import evaluate_exam_with_ocr_to_json
from .report import generate_report
from.get_score import extract_score_from_report
import json 

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
    exams = StudentExam.objects.filter(student=request.user)
    return render(request, 'student_dashboard/student_dashboard.html', {'exams': exams})
@login_required
# Teacher Dashboard showing created exams
def teacher_dashboard(request):
    exams = Exam.objects.all()  # List all created exams
    return render(request, 'teacher/teacher_dashboard.html', {'exams': exams})

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
def student_exam_fill(request):
    if request.method == 'POST':
        form = StudentExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.student = request.user  # Link to logged-in student
            exam.save()
            return redirect('student_dashboard')  # Redirect after success
    else:
        form = StudentExamForm()
    
    return render(request, 'student_dashboard/exam_fill.html', {'form': form})




def student_info(request):
    return HttpResponse("Working on it")

def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = ExamForm()
    return render(request, 'teacher/create_exam.html', {'form': form})

def view_exam_submissions(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    submissions = StudentExam.objects.filter(
        exam_type=exam.exam_type,
        year=exam.year,
    )

    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        action = request.POST.get('action')
        submission = get_object_or_404(StudentExam, pk=submission_id)

        # 🔥 Handle File Upload
        if action == 'upload':
            if 'ocr_answer_sheet' in request.FILES:
                submission.ocr_answer_sheet = request.FILES['ocr_answer_sheet']
                submission.save()
                messages.success(request, f"OCR answer sheet uploaded for {submission.student.username}.")
            else:
                messages.error(request, "No file uploaded.")
            return redirect('view_exam_submissions', exam_id=exam_id)

        # 🔥 Handle Evaluation
        elif action == 'evaluate':
            if not submission.ocr_answer_sheet:
                messages.error(request, "Upload OCR answer sheet before evaluating.")
                return redirect('view_exam_submissions', exam_id=exam_id)

            try:
                # Step 1: Run OCR on uploaded file
                ocr_text = generate_ocr(submission.ocr_answer_sheet.path)

                # Step 2: Extract question paper content
                question_paper_text = question_answer_content(exam.question_paper.path)

                # Step 3: Preprocess OCR text (match answers to questions)
                preprocessed_content = preprocess_ocr_question_wise(ocr_text, question_paper_text)

                # Step 4: Load the answer key
                answer_key_content = question_answer_content(exam.answer_key.path)

                # Step 5: Evaluate answers
                evaluation_result = evaluate_exam_with_ocr_to_json(preprocessed_content, answer_key_content)

                # Step 6: Generate report and calculate scores
                report = generate_report(evaluation_result)

                # Step 7: Save results
                submission.is_evaluated = True
                submission.evaluation_report = report  # Assuming you have this field
                submission.total_score = extract_score_from_report(report)  # Function to parse score
                submission.save()

                messages.success(request, f"Evaluation completed for {submission.student.username}.")

            except Exception as e:
                messages.error(request, f"Error during evaluation: {e}")

            return redirect('view_exam_submissions', exam_id=exam_id)

    context = {
        'exam': exam,
        'submissions': submissions,
    }
    return render(request, 'teacher/view_exam_submissions.html', context)


def view_result(request, submission_id):
    submission = get_object_or_404(StudentExam, id=submission_id)

    # Parse the evaluation report JSON
    evaluation_report = []
    if submission.evaluation_report:
        try:
            evaluation_report = json.loads(submission.evaluation_report)
        except json.JSONDecodeError:
            evaluation_report = []

    context = {
        'submission': submission,
        'evaluation_report': evaluation_report
    }
    return render(request, 'teacher/view_results.html', context)