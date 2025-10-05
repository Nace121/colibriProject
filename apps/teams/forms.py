
from django import forms
from django.utils.translation import gettext_lazy as _
from apps.students.models import Student
from .models import Team, TeamInvitation

class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "specialization"]

class TeamInviteForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        label=_("Étudiant à inviter"),
        help_text=_("Sélectionne un étudiant à inviter dans l'équipe."),
    )

    class Meta:
        model = TeamInvitation
        fields = ["student"]
