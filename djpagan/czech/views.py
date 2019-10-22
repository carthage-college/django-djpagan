from django.conf import settings
from django.shortcuts import render

from djpagan.czech.forms import ReimbursementForm


def reimbursement(request):

    form = ReimbursementForm()

    return render(
        request, 'czech/reimbursement/form.html', {'form': form,}
    )
