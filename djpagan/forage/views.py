# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from djauth.decorators import portal_auth_required
from djpagan.forage.forms import MealPlanForm
from djpagan.forage.models import MealPlan


@portal_auth_required(
    session_var='DJPAGAN_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def mealplan(request):
    """Check for meal plan status."""
    data = None
    if request.method == 'POST':
        form = MealPlanForm(
            request.POST,
            use_required_attribute=settings.REQUIRED_ATTRIBUTE,
        )
        if form.is_valid():
            cd = form.cleaned_data
            mealplan = MealPlan.objects.create(
                user=user,
                level=level,
                status=status,
                location=data['location'],
            )
    else:
        form = MealPlanForm(use_required_attribute=settings.REQUIRED_ATTRIBUTE)

    return render(
        request,
        'forage/form.html',
        {'form': form, 'data': data},
    )
