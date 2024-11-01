# -*- coding: utf-8 -*-

from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from djauth.views import loggedout
from djpagan.core import views


admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    # we don't want users created through django admin
    path(
        'admin/auth/user/add/',
        RedirectView.as_view(url=reverse_lazy('auth_login'))
    ),
    # auth
    path(
        'accounts/login/', auth_views.LoginView.as_view(),
        {'template_name': 'registration/login.html'},
        name='auth_login'
    ),
    path(
        'accounts/logout/', auth_views.LogoutView.as_view(),
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout'
    ),
    path(
        'accounts/loggedout/', loggedout,
        {'template_name': 'registration/logged_out.html'},
        name='auth_loggedout'
    ),
    path(
        'accounts/',
        RedirectView.as_view(url=reverse_lazy('auth_login'))
    ),
    path(
        'denied/',
        #RedirectView.as_view(url=reverse_lazy('remission')),
        #RedirectView.as_view(url=reverse_lazy('mealplan')),
        TemplateView.as_view(template_name='denied.html'),

        name='access_denied',
    ),
    # django admin and loginas
    path('rocinante/', admin.site.urls),
    # tutition stuff
    path('tuition/', include('djpagan.tuition.urls')),
    # dashboard home
    path('', views.home, name='home'),
]
