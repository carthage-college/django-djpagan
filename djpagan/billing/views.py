import datetime

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import Http404

from djpagan.core.utils import get_objects
from djpagan.billing.forms import SearchBridgedForm
from djpagan.billing.forms import SearchChequeForm
from djpagan.billing.forms import SearchJournalForm
from djpagan.billing.forms import SearchTransactionForm
from djpagan.billing.sql import ALL_TRANSACTIONS
from djpagan.billing.sql import BRIDGED_CLASSES
from djpagan.billing.sql import BRIDGED_CLASSES_STUDENTS
from djpagan.billing.sql import CHEQUE_NUMBER
from djpagan.billing.sql import JOURNAL_TRANSACTIONS

from djauth.decorators import portal_auth_required

from djtools.utils.convert import str_to_class

import os

STATUS = settings.VOID_STATUS


@portal_auth_required(
    group='StudentAccounts',
    session_var='DJPAGAN_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
@staff_member_required
def search(request, tipo):

    sql = None
    objects = None

    # check for a valid template or redirect home
    try:
        template = 'billing/search_{}.html'.format(tipo)
        os.stat(os.path.join(settings.BASE_DIR, 'templates', template))
    except:
        return HttpResponseRedirect( reverse_lazy('home') )

    form_class = str_to_class(
        'djpagan.billing.forms', 'Search{}Form'.format(tipo.title())
    )

    if not form_class:
        raise Http404

    if request.method == 'POST':
        form = form_class(request.POST.copy(), prefix=tipo)
        if form.is_valid():
            data = form.cleaned_data
            stat = STATUS
            if data.get('include_voids'):
                stat = ''
            # various types of search parameters
            if tipo == 'journal':
                sql = JOURNAL_TRANSACTIONS(
                    vch_ref = data['journal_type'],
                    journal_no = data['journal_number'],
                    stat = stat
                )
            elif tipo == 'bridged':
                course_no = data['course_no']
                year = datetime.date.today().year - 2
                bridged = get_objects(
                    BRIDGED_CLASSES(
                        year = year,
                        course_no = 'AND crs_rec.crs_no="{}"'.format(course_no)
                    )
                )
                sql = BRIDGED_CLASSES_STUDENTS(
                    year = bridged[0].yr, course_no = data['course_no'],
                    a_sess = bridged[0].a_sess, b_sess = bridged[0].b_sess
                )
            elif tipo == 'transaction':
                sql = ALL_TRANSACTIONS(
                    student_id = data['student_number'],
                    stat = stat
                )
            elif tipo == 'cheque':
                sql = CHEQUE_NUMBER(
                    cheque_number = data['cheque_number'],
                    stat = stat
                )
            elif tipo == 'test':
                pass

            objects = get_objects(sql)
    else:
        form = form_class(prefix=tipo)

    return render(
        request, template, {'form':form, 'objects': objects, 'sql':sql}
    )
