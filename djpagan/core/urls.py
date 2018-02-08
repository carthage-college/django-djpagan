from django.contrib import admin
from django.conf.urls import include, url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView, TemplateView

from djpagan.core import views

from djauth.views import loggedout

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    # we don't want users created through django admin
    url(
        r'^admin/auth/user/add/$',
        RedirectView.as_view(url=reverse_lazy('auth_login'))
    ),
    url(r'^admin/', include(admin.site.urls)),
    # auth
    url(
        r'^accounts/login/$',auth_views.login,
        {'template_name': 'accounts/login.html'},
        name='auth_login'
    ),
    url(
        r'^accounts/logout/$',auth_views.logout,
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout'
    ),
    url(
        r'^accounts/loggedout/$', loggedout,
        {'template_name': 'accounts/logged_out.html'},
        name='auth_loggedout'
    ),
    url(
        r'^accounts/$',
        RedirectView.as_view(url=reverse_lazy('auth_login'))
    ),
    url(
        r'^denied/$',
        TemplateView.as_view(
            template_name='denied.html'
        ), name='access_denied'
    ),
    # billing search and reports
    url(
        r'^billing/', include('djpagan.billing.urls')
    ),
    # search students by various parameters
    url(
        r'^student/search/$', views.search_students,
        name='search_students'
    ),
    url(
        r'^student/(?P<sid>\d+)/$', views.student_detail,
        name='student_detail'
    ),
    # dashboard home
    url(
        r'^$', views.home, name='home'
    ),
]
