from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.http import Http404

from djpagan.core.utils import get_objects
from djpagan.billing.forms import *
from djpagan.billing.sql import *

from djzbar.decorators.auth import portal_auth_required

from djtools.utils.convert import str_to_class
from djtools.fields import TODAY

import os


@portal_auth_required(
    'StudentAccounts', 'DJPAGAN_AUTH', reverse_lazy('access_denied')
)
def search(request, tipo):

    sql = None
    objects = None

    if not tipo:
        raise Http404

    # check for a valid template or redirect home
    try:
        template = 'billing/search_{}.html'.format(tipo)
        os.stat(os.path.join(settings.ROOT_DIR, 'templates', template))
    except:
        return HttpResponseRedirect( reverse_lazy('home') )

    form_class = str_to_class(
        'djpagan.billing.forms', 'Search{}Form'.format(tipo.title())
    )

    if not form_class:
        raise Http404

    if request.method == 'POST':
        form = form_class(request.POST.copy())
        if form.is_valid():
            data = form.cleaned_data
            if tipo == 'transaction':
                stat = ''
                if data['include_voids']:
                    stat = 'AND vch_rec.stat <> "V"'

                sql = JOURNAL_TRANSACTIONS(
                    vch_ref = data['journal_type'],
                    journal_no = data['journal_number'],
                    stat = stat
                )
            elif tipo == 'bridged':
                course_no = data['course_no']
                year = TODAY.year - 2
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
            elif tipo == 'test':
                pass

            objects = get_objects(sql)
    else:
        form = form_class()

    return render(
        request, template, {'form':form, 'objects': objects, 'sql':sql}
    )
