# -*- coding: utf-8 -*-

from django import forms
from djpagan.forage.models import LOCATION_CHOICES


class MealPlanForm(forms.Form):
    """Meal plan status form."""

    cid = forms.CharField(label="College ID", required=True)
    location = forms.TypedChoiceField(
        label="Location",
        choices=LOCATION_CHOICES,
        widget=forms.RadioSelect,
        required=True,
    )
