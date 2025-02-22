from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

class Exam(models.Model):
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]

    EXAM_TYPE_CHOICES = [
        ('CAT 1', 'CAT 1'),
        ('CAT 2', 'CAT 2'),
    ]
    
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    subject = models.CharField(max_length=100)
    question_paper = models.FileField(upload_to='question_papers/')
    answer_key = models.FileField(upload_to='answer_keys/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.exam_type} ({self.get_year_display()})"
    
class StudentExam(models.Model):
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]

    EXAM_TYPE_CHOICES = [
        ('CAT 1', 'CAT 1'),
        ('CAT 2', 'CAT 2'),
    ]
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='submissions',null=True,blank=True)  # New field
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    staff_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)
    ocr_answer_sheet = models.FileField(upload_to='ocr_answer_sheets/', null=True, blank=True)
    is_evaluated = models.BooleanField(default=False)
    total_score = models.FloatField(null=True, blank=True)
    evaluation_report = models.TextField(null=True, blank=True)  # New field

    def __str__(self):
        return f"{self.student.username} - {self.subject} ({self.exam_type})"