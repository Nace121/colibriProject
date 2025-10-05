from django import forms
from .models import Student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["university","level","specialization","bio","cv","skills"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows":4})
        }
