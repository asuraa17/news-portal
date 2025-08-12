from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter a username"}
        ),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your email"}
        ),
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter your password"}
        ),
    )

    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Confirm password"}
        ),
    )

    class Meta(UserCreationForm.Meta):
        model =  User
        fields = ("username","email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email