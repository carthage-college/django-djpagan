from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from djpagan.billing.forms import *
from djpagan.billing.sql import JOURNAL_TYPES
from djpagan.core.utils import get_objects

from djzbar.decorators.auth import portal_auth_required


@portal_auth_required(
    group='StudentAccounts', session_var='DJPAGAN_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def home(request):

    form_bridged = SearchBridgedForm(prefix='bridged')
    form_cheque = SearchChequeForm(prefix='cheque')
    form_journal = SearchJournalForm(prefix='journal')
    form_transaction = SearchTransactionForm(prefix='transaction')

    return render(
        request, 'core/home.html',
        {
            'form_bridged':form_bridged,
            'form_cheque':form_cheque,
            'form_journal':form_journal,
            'form_transaction':form_transaction
        }
    )
