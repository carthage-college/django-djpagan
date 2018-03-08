from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from djpagan.core.sql import SUBSIDIARY_BALANCES
from djpagan.core.sql import PROGRAM_ENROLLMENT
from djpagan.core.sql import ACCOUNT_NOTES
from djpagan.core.sql import SESSION_DETAILS
from djpagan.core.sql import SEARCH_STUDENTS

from djpagan.core.forms import SearchStudentsForm
from djpagan.core.utils import get_objects
from djpagan.billing.forms import SearchBridgedForm
from djpagan.billing.forms import SearchChequeForm
from djpagan.billing.forms import SearchJournalForm
from djpagan.billing.forms import SearchTransactionForm

from djzbar.decorators.auth import portal_auth_required
from djzbar.utils.informix import get_session

EARL = settings.INFORMIX_EARL


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
def search_students(request):
    sql = None
    students = None
    if request.method == 'POST':
        form = SearchStudentsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            student = data['student']
            try:
                sid = int(student)
                return HttpResponseRedirect(
                    reverse_lazy('student_detail', args=[sid])
                )
            except:
                sql = SEARCH_STUDENTS(
                    lastname = student
                )
                students = get_objects(sql)
    else:
        form = SearchStudentsForm()

    return render(
        request, 'core/search_students.html',
        {'form':form, 'students':students,'sql':sql}
    )


@portal_auth_required(
    group='StudentAccounts', session_var='DJPAGAN_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def student_detail(request, sid):

    enrollment = get_objects(PROGRAM_ENROLLMENT(student_number=sid), True)
    balances = get_objects(SUBSIDIARY_BALANCES(student_number=sid), True)
    notes = get_objects(ACCOUNT_NOTES(student_number=sid), True)
    # we have to use session method here because of the temp table
    session = get_session(EARL)

    sql = SESSION_DETAILS(
        student_number = sid,
        start_date = settings.ORDERED_TERMS_START_DATE
    )

    details = session.execute(sql).first()

    session.close()

    return render(
        request, 'core/detail_student.html', {
            'enrollment':enrollment, 'balances':balances,
            'notes':notes, 'details':details,
        }
    )
