from django.conf import settings
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404

from djskeletor.myapp.forms import MyForm
from djtools.utils.mail import send_mail

def myview(request, pid=None):
    if settings.DEBUG:
        TO_LIST = [settings.SERVER_EMAIL,]
    else:
        TO_LIST = [settings.MY_APP_EMAIL,]
    BCC = settings.MANAGERS

    if request.method=='POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
            email = settings.DEFAULT_FROM_EMAIL
            if data.email:
                email = data.email
            subject = "[Submit] {} {}".format(data.first_name,data.last_name)
            send_mail(
                request,TO_LIST, subject, email,'myapp/email.html', data, BCC
            )
            return HttpResponseRedirect(
                reverse_lazy('myapp_success')
            )
    else:
        form = MyForm()
    return render(
        request, 'myapp/form.html',
        {'form': form,}
    )

def search(request):
    return render(
        request, 'myapp/search.html', {}
    )

