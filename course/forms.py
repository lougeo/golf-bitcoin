from django import forms

from .models import Scorecard

"""
Admin Forms
"""


class ScorecardAdminForm(forms.ModelForm):
    class Meta:
        model = Scorecard
        fields = "__all__"
