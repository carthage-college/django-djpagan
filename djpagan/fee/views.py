from django.conf import settings
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
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

from djimix.decorators.auth import portal_auth_required
from djimix.core.database import get_connection, xsql

import csv


@portal_auth_required(
    group='StudentAccounts', session_var='DJPAGAN_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def student_balance_late_fee(request):

    if request.POST:
        connection = get_connection()
        # automatically closes the connection after leaving 'with' block
        with connection:

            # ordered terms temp table
            sql = ORDERED_TERMS_TEMP(
                start_date = settings.ORDERED_TERMS_START_DATE
            )
            xsql(sql, connection, settings.INFORMIX_DEBUG)

            # latest terms temp table
            xsql(LATEST_TERM_TEMP, connection, settings.INFORMIX_DEBUG)

            # sa balances temp table
            xsql(SA_BALANCES_TEMP, connection, settings.INFORMIX_DEBUG)

            # pc balances temp table
            xsql(PC_BALANCES_TEMP, connection, settings.INFORMIX_DEBUG)

            # ca balances temp table
            xsql(CA_BALANCES_TEMP, connection, settings.INFORMIX_DEBUG)

            # ca1 balances temp table
            xsql(CA1_BALANCES_TEMP, connection, settings.INFORMIX_DEBUG)

            # wo balances temp table
            xsql(WO_BALANCES_TEMP, connection, settings.INFORMIX_DEBUG)

            # student balance late fee
            students = xsql(
                STUDENT_BALANCE_LATE_FEE, connection, settings.INFORMIX_DEBUG
            ).fetchall()

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
