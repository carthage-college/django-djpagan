# -*- coding: utf-8 -*-

from captcha.fields import CaptchaField
from django import forms
from djpagan.tuition.models import GenericChoice
from djpagan.tuition.models import Remission
from djtools.fields import BINARY_CHOICES
from djtools.fields.localflavor import USPhoneNumberField


ASSISTANCE_CHOICES = GenericChoice.objects.filter(
    tags__name__in=['Assistance'],
).filter(active=True).order_by('ranking')


class RemissionForm(forms.ModelForm):
    """Tuition assistance form."""

    income = forms.ChoiceField(
        label="Is the employee's adjusted gross income greater than 60,000?",
        help_text="If no, the employee will be required to complete a FAFSA.",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
    )
    phone = USPhoneNumberField(help_text='Format: XXX-XXX-XXXX')
    assistance = forms.ModelMultipleChoiceField(
        label="Student is applying as...",
        queryset=ASSISTANCE_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        help_text="Check all that apply.",
    )
    captcha = CaptchaField()

    class Meta:
        """Information about the data class model."""

        model = Remission
        exclude = (
            'user',
            'created_at',
            'updated_at',
            'updated_by',
            'percentage',
            'approved',
            'approved_email',
        )
