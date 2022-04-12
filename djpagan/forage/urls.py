# -*- coding: utf-8 -*-

from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from djpagan.forage import views


urlpatterns = [
    path('meal-plan/', views.mealplan, name='mealplan'),
    path('', RedirectView.as_view(url=reverse_lazy('mealplan'))),
]
