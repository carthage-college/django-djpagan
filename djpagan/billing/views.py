from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from djpagan.billing.forms import SearchTransactionForm
from djpagan.billing.sql import TRANSACTIONS
from djpagan.core.utils import get_objects

from djzbar.decorators.auth import portal_auth_required


@portal_auth_required(
    'StudentAccounts', 'DJPAGAN_AUTH', reverse_lazy('access_denied')
)
def search(request, tipo=None):

    objects = None

    if request.method == 'POST':
        form = SearchTransactionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            stat = ''
            if data['include_voids']:
                stat = 'AND vch_rec.stat <> "V"'

            sql = TRANSACTIONS(
                vch_ref = data['journal_type'],
                journal_no = data['journal_number'],
                stat = stat
            )
            objects = get_objects(sql)
    else:
        form = SearchTransactionForm()

    return render(
        request, 'billing/search_transaction.html',
        {'form':form, 'objects': objects}
    )
