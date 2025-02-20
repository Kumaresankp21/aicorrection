from django import forms
from django.contrib.auth.models import User
from app.models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)  # Role selection

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
