# -*- coding: utf-8 -*-

import datetime

from django import forms
from djpagan.billing.sql import BRIDGED_CLASSES, JOURNAL_TYPES
from djpagan.core.utils import get_objects


class SearchJournalForm(forms.Form):

    journal_type = forms.CharField()
    journal_number = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': 'Journal number'})
    )
    include_voids = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(SearchJournalForm, self).__init__(*args, **kwargs)

        objects = get_objects(JOURNAL_TYPES)
        choices = [("","---journal type---")]
        for o in objects:
            choices.append((o.vch_ref, "{} {}".format(o.vch_ref,o.txt)))
            #choices.append((o[0], "{} {}".format(o[0],o[1])))

        self.fields['journal_type'] = forms.ChoiceField(
            choices=choices
        )


class SearchBridgedForm(forms.Form):

    course_no = forms.CharField(label = "Course")

    def __init__(self, *args, **kwargs):
        super(SearchBridgedForm, self).__init__(*args, **kwargs)

        year = datetime.date.today().year - 2
        objects = get_objects(BRIDGED_CLASSES(year = year, course_no = ''))

        choices = [("","---bridged classes---")]
        for o in objects:
            choices.append((
                o.crs_no, "[{}] {}".format(o.crs_no, o.course_title)
            ))

        self.fields['course_no'] = forms.ChoiceField(
            choices=choices
        )


class SearchTransactionForm(forms.Form):

    student_number = forms.IntegerField(
        label = "Student ID",
        widget=forms.TextInput(attrs={'placeholder': 'Student ID'})
    )
    include_voids = forms.BooleanField(required=False)


class SearchChequeForm(forms.Form):

    cheque_number = forms.IntegerField(
        label = "Check number",
        widget=forms.TextInput(attrs={'placeholder': 'Check number'})
    )
    include_voids = forms.BooleanField(required=False)

