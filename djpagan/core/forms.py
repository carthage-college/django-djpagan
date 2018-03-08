# -*- coding: utf-8 -*-
from django import forms


class StudentNumberForm(forms.Form):

    student_number = forms.IntegerField(
        label = "Student ID",
        widget=forms.TextInput(attrs={'placeholder': 'Student ID'})
    )


class SearchStudentsForm(forms.Form):

    student = forms.CharField(
        label = "Last Name or ID",
        widget=forms.TextInput(attrs={'placeholder': 'Last Name or ID'})
    )
