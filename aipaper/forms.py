from django import forms
from django.contrib.auth.models import User
from app.models import Profile,AnswerSheet

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)  # Role selection

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
class AnswerSheetUploadForm(forms.ModelForm):
    class Meta:
        model = AnswerSheet
        fields = ['year', 'exam_type', 'staff_name', 'subject', 'answer_file']
        widgets = {
            'year': forms.Select(attrs={'class': 'form-control'}),
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'staff_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Staff Name'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject'}),
            'answer_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

