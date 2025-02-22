from django import forms
from django.contrib.auth.models import User
from app.models import Profile,StudentExam,Exam

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)  # Role selection

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        
class StudentExamForm(forms.ModelForm):
    class Meta:
        model = StudentExam
        fields = ['year', 'exam_type', 'staff_name', 'subject']
        widgets = {
            'year': forms.Select(attrs={'class': 'form-control'}),
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'staff_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Staff Name'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject'}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_type', 'year', 'subject', 'question_paper', 'answer_key']
        widgets = {
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject'}),
            'question_paper': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'answer_key': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
