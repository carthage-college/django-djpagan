from django.urls import path

from djpagan.czech.views import reimbursement


urlpatterns = [
    path('reimbursement/', reimbursement, name='reimbursement_form'),
]
