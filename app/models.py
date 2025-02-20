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
    
class AnswerSheet(models.Model):
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

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES,null=True,blank=True)
    staff_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    answer_file = models.FileField(upload_to='answer_sheets/')
    is_graded = models.BooleanField(default=False)
    grade = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.subject} ({self.exam_type})"