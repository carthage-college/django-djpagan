from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from djpagan.core.sql import MOST_RECENT_TERM
from djpagan.core.forms import MostRecentTermForm
from djpagan.core.utils import get_objects
from djpagan.billing.forms import SearchBridgedForm
from djpagan.billing.forms import SearchChequeForm
from djpagan.billing.forms import SearchJournalForm
from djpagan.billing.forms import SearchTransactionForm

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


@portal_auth_required(
    group='StudentAccounts', session_var='DJPAGAN_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def most_recent_term(request):

    student = None
    if request.method == 'POST':
        form = MostRecentTermForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            sql = MOST_RECENT_TERM(
                student_number = data['student_number']
            )
            student = get_objects(sql)
    else:
        form = MostRecentTermForm()

    return render(
        request, 'core/most_recent_term.html',
        {'form':form, 'student':student,}
    )
