from django.conf import settings
from django.shortcuts import render
from django.template import loader
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse

from djpagan.core.forms import StudentNumberForm
from djpagan.fee.sql import LATEST_TERM_TEMP
from djpagan.fee.sql import ORDERED_TERMS_TEMP
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
        form = StudentNumberForm(request.POST, prefix='late_fee')
        if form.is_valid():
            cd = form.cleaned_data
            # create database session
            session = get_session(EARL)

            # ordered terms temp table
            sql = ORDERED_TERMS_TEMP(
                start_date = settings.ORDERED_TERMS_START_DATE
            )
            session.execute(sql)

            # latest terms temp table
            sql = LATEST_TERM_TEMP
            session.execute(sql)

            # student balance late fee

            sql = STUDENT_BALANCE_LATE_FEE(
                student_number = cd['student_number']
            )
            students = session.execute(sql)

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

    else:
        form = StudentNumberForm(prefix='late_fee')


    return render(
        request, 'fee/student_balance_late_fee.html', { 'form':form, }
    )
