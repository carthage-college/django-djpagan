from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from djpagan.financialaid import views


urlpatterns = [
    path('wisact284/', views.wisact284, name='wisact284'),
    path('', RedirectView.as_view(url=reverse_lazy('home'))),
]
