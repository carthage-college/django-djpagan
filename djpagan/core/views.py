from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from djpagan.billing.forms import SearchTransactionForm
from djpagan.billing.sql import JOURNAL_TYPES
from djpagan.core.utils import get_objects

from djzbar.decorators.auth import portal_auth_required


@portal_auth_required(
    'StudentAccounts', 'DJPAGAN_AUTH', reverse_lazy('access_denied')
)
def home(request):

    form_journal = SearchTransactionForm()

    return render(
        request, 'core/home.html',
        {'form_journal':form_journal,}
    )
