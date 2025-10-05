from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterStudentForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.Types.STUDENT
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class RegisterCompanyForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.Types.COMPANY
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
