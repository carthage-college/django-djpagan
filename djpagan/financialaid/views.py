from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy

from djpagan.financialaid.forms import WisAct284Form
from djpagan.financialaid.sql import WIS_ACT_284_SQL
from djpagan.financialaid.utils import csv_gen

from djzbar.decorators.auth import portal_auth_required
from djzbar.utils.informix import do_sql

import csv
import time

EARL = settings.INFORMIX_EARL
DEBUG = settings.INFORMIX_DEBUG


@portal_auth_required(
    group='carthageStaffStatus', session_var='DJPAGAN_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def wisact284(request):

    sql = None
    test = False
    objects = None
    if request.method=='POST':
        form = WisAct284Form(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            stat = '"AA","AD","AP","EA"'
            if data['dispersed']:
                stat = '"AD"'
            sql = WIS_ACT_284_SQL(amt_stat = stat)
            objects = do_sql(sql, earl=EARL)

            datetimestr = time.strftime("%Y%m%d%H%M%S")
            # College Cost Meter file name
            ccmfile = (
                'CCM-{}.csv'.format(datetimestr)
            )

            response = HttpResponse(content_type="text/csv; charset=utf-8")
            content = 'attachment; filename={}'.format(ccmfile)
            response['Content-Disposition'] = content

            writer = csv.writer(response)
            if data['headers']:
                test = True
            csv_gen(objects, writer, test)

            return response

    else:
        form = WisAct284Form()

    return render(
        request, 'financialaid/wisact284.html',
        {'form':form, 'objects':objects, 'sql':sql}
    )
