# -*- coding: utf-8 -*-
from django import forms


class MostRecentTermForm(forms.Form):

    student_number = forms.CharField(
        label = "Student ID",
        widget=forms.TextInput(attrs={'placeholder': 'Student ID'})
    )
