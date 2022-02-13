# -*- coding: utf-8 -*-

from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from djpagan.tuition import views


urlpatterns = [
    path('remission/', views.remission, name='remission'),
    path(
        'remission/success/',
        TemplateView.as_view(template_name='tuition/remission/success.html'),
        name='remission_success',
    ),
    path('', RedirectView.as_view(url=reverse_lazy('remission'))),
]
