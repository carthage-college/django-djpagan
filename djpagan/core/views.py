from django.conf import settings
from django.shortcuts import render

from djtools.decorators.auth import group_required


@group_required('StudentAccounts')
def home(request):

    return render(request, 'core/home.html', {})
