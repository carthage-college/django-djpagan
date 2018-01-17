# -*- coding: utf-8 -*-
from django import forms

from djpagan.billing.sql import JOURNAL_TYPES
from djpagan.core.utils import get_objects

from djtools.fields import BINARY_CHOICES


class SearchTransactionForm(forms.Form):

    journal_type = forms.CharField()
    journal_number = forms.CharField()
    include_voids = forms.CharField(
        widget=forms.RadioSelect(choices=BINARY_CHOICES)
    )

    def __init__(self, *args, **kwargs):
        super(SearchTransactionForm, self).__init__(*args, **kwargs)

        objects = get_objects(JOURNAL_TYPES)
        choices = [('','---choose a journal type---')]
        for o in objects:
            choices.append((o.vch_ref, "{} {}".format(o.vch_ref,o.txt)))

        self.fields['journal_type'] = forms.ChoiceField(
            choices=choices
        )
