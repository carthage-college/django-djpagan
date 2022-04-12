# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from djauth.decorators import portal_auth_required
from djimix.core.utils import get_connection
from djimix.core.utils import xsql
from djpagan.forage.forms import MealPlanForm
from djpagan.forage.models import MealPlan


@portal_auth_required(
    session_var='DJPAGAN_AUTH',
    redirect_url=reverse_lazy('access_denied')
)
def mealplan(request):
    """Check for meal plan status."""
    cd = None
    mealplan = None
    if request.method == 'POST':
        form = MealPlanForm(
            request.POST,
            use_required_attribute=settings.REQUIRED_ATTRIBUTE,
        )
        if form.is_valid():
            cd = form.cleaned_data
            cid = cd['cid']
            sql = """
                SELECT
                    TRIM(NVL(meal_plan_type, '')) as meal_plan,
                    cvid_rec.ldap_name as username,
                    (TRIM(cvid_rec.ldap_name) || '@carthage.edu') AS email,
                    id_rec.lastname, id_rec.firstname
                FROM
                    id_rec
                LEFT JOIN
                    cvid_rec
                ON
                    id_rec.id = cvid_rec.cx_id
                LEFT JOIN
                    stu_serv_rec
                ON
                    id_rec.id = stu_serv_rec.id
                WHERE
                    stu_serv_rec.yr = 2022
                AND
                    stu_serv_rec.sess = 'RC'
                AND id_rec.id = {0}
            """.format(cid)
            with get_connection(settings.INFORMIX_ODBC) as connection:
                student = xsql(sql, connection, key=settings.INFORMIX_DEBUG).fetchone()
                if student:
                    status = True
                    level = student.meal_plan
                else:
                    status = False
                    level = ''
                    sql = """
                        SELECT
                            cvid_rec.ldap_name as username,
                            (TRIM(cvid_rec.ldap_name) || '@carthage.edu') AS email,
                            id_rec.lastname, id_rec.firstname
                        FROM
                            id_rec
                        LEFT JOIN
                            cvid_rec
                        ON
                            id_rec.id = cvid_rec.cx_id
                        WHERE
                            id_rec.id = {0}
                    """.format(cid)
                    student = xsql(sql, connection, key=settings.INFORMIX_DEBUG).fetchone()
            if student:
                # check for an exisiting user
                user = User.objects.filter(pk=cid).first()
                if not user:
                    password = User.objects.make_random_password(length=32)
                    user = User.objects.create(
                        pk=cid,
                        username=student.username,
                        email=student.email,
                        last_name=student.lastname,
                        first_name=student.firstname,
                        last_login=datetime.datetime.now(),
                    )
                    user.set_password(password)
                    grup = Group.objects.get(name__iexact=settings.STUDENT_GROUP)
                    if not user.groups.filter(name=grup).exists():
                        grup.user_set.add(user)
                    user.save()
                # create the mealplan instance
                mealplan = MealPlan.objects.create(
                    user=user,
                    level=level,
                    status=status,
                    location=cd['location'],
                )
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Meal Plan for student with the ID {0}: {1}.".format(cid, mealplan.level),
                    extra_tags='alert-success',
                )
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "We could not find a student with the ID {0}.".format(cid),
                    extra_tags='alert-warning',
                )
    else:
        form = MealPlanForm(use_required_attribute=settings.REQUIRED_ATTRIBUTE)

    return render(
        request,
        'forage/form.html',
        {'form': form, 'mealplan': mealplan},
    )