# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text='Optional')

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=None
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        help_text=None
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts = {
            "username": None,
        }
