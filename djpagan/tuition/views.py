# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from djpagan.tuition.forms import RemissionForm
from djtools.utils.mail import send_mail


@login_required
def remission(request):
    """Tuition assistance form."""
    if request.method == 'POST':
        form = RemissionForm(
            request.POST,
            use_required_attribute=settings.REQUIRED_ATTRIBUTE,
        )
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.updated_by = request.user
            data.save()
            # m2m save for GenericChoice relationships
            form.save_m2m()
            # notify HR
            to_list = settings.TUITION_REMISSION_NEW_LIST
            if settings.DEBUG:
                remission.to_list = to_list
                to_list = [settings.MANAGERS[0][1]]

            subject = "[Tuition Remission] Submission: {0}, {1}".format(
                data.user.last_name, data.user.first_name,
            )
            frum = settings.SERVER_MAIL
            sent = send_mail(
                request,
                to_list,
                subject,
                frum,
                'tuition/remission/email.html',
                data,
                reply_to=[frum,],
                bcc = [settings.MANAGERS[0][1]],
            )
            return HttpResponseRedirect(reverse_lazy('remission_success'))
    else:
        form = RemissionForm(use_required_attribute=settings.REQUIRED_ATTRIBUTE)

    return render(request, 'tuition/remission/form.html', {'form': form})
