from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from djpagan.fee import views


urlpatterns = [
    path(
        'student-balance-late-fee/',
        views.student_balance_late_fee, name='student_balance_late_fee'
    ),
    path('', RedirectView.as_view(url=reverse_lazy('home'))),
]
