
from django import forms
from apps.teams.models import Team
from .models import Application

class ApplicationCreateForm(forms.ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.none(), label="Équipe")

    class Meta:
        model = Application
        fields = ["team", "cover_letter", "proposed_price", "proposed_duration"]
        widgets = {"cover_letter": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None and user.is_authenticated:
            self.fields["team"].queryset = Team.objects.filter(members__user=user).distinct()
