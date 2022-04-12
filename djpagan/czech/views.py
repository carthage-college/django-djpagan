from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import reverse_lazy
from djauth.decorators import portal_auth_required
from djpagan.czech.forms import ReimbursementForm


@portal_auth_required(
    group='StudentAccounts',
    session_var='DJPAGAN_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
@staff_member_required
def reimbursement(request):
    form = ReimbursementForm()
    return render(request, 'czech/reimbursement/form.html', {'form': form})
