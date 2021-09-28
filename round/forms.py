from django.contrib.admin.widgets import AdminDateWidget
from django import forms

from .models import Round


class RoundAdminForm(forms.ModelForm):
    tee_time = forms.DateTimeField(
        input_formats=["%Y-%d-%m %H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
        ),
    )
