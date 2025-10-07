
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "category",
            "required_skills",
            "budget",
            "duration",
            "deadline",
            "location",
            "remote_allowed",
            "status",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }
