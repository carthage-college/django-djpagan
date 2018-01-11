# -*- coding: utf-8 -*-

from django import forms

from djskeletor.myapp.models import MyModel

class MyForm(forms.ModelForm):

    class Meta:
        model = MyModel
        # either fields or exclude is required
        fields = '__all__'

