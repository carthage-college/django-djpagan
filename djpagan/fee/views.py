from django.conf import settings
from django.shortcuts import render
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
# order in which we execute them
from djpagan.fee.sql import ORDERED_TERMS_TEMP
from djpagan.fee.sql import LATEST_TERM_TEMP
from djpagan.fee.sql import SA_BALANCES_TEMP
from djpagan.fee.sql import PC_BALANCES_TEMP
from djpagan.fee.sql import CA_BALANCES_TEMP
from djpagan.fee.sql import CA1_BALANCES_TEMP
from djpagan.fee.sql import WO_BALANCES_TEMP
from djpagan.fee.sql import STUDENT_BALANCE_LATE_FEE

from djzbar.decorators.auth import portal_auth_required
from djzbar.utils.informix import get_session

import csv

EARL = settings.INFORMIX_EARL


@portal_auth_required(
    group='StudentAccounts', session_var='DJPAGAN_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def student_balance_late_fee(request):

    if request.POST:
        # create database session
        session = get_session(EARL)

        # ordered terms temp table
        sql = ORDERED_TERMS_TEMP(
            start_date = settings.ORDERED_TERMS_START_DATE
        )
        session.execute(sql)

        # latest terms temp table
        session.execute(LATEST_TERM_TEMP)

        # sa balances temp table
        session.execute(SA_BALANCES_TEMP)

        # pc balances temp table
        session.execute(PC_BALANCES_TEMP)

        # ca balances temp table
        session.execute(CA_BALANCES_TEMP)

        # ca1 balances temp table
        session.execute(CA1_BALANCES_TEMP)

        # wo balances temp table
        session.execute(WO_BALANCES_TEMP)

        # student balance late fee
        students = session.execute(STUDENT_BALANCE_LATE_FEE)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            'student_balance_late_fee'
        )

        t = loader.get_template('fee/student_balance_late_fee.txt')
        context = {
            'students': students,
        }
        response.write(t.render(context, request))

        writer = csv.writer(response)

        return response

    return render(
        request, 'fee/student_balance_late_fee.html'
    )
