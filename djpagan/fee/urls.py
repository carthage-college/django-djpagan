from django.conf.urls import url

from djpagan.fee import views


urlpatterns = [
    url(
        r'^student-balance-late-fee/$',
        views.student_balance_late_fee, name='student_balance_late_fee'
    ),
]
