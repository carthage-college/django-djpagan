from django.conf.urls import include, url
from django.views.generic import RedirectView, TemplateView

from django.contrib import admin

admin.autodiscover()

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = [
    url(
        r'^admin/', include(admin.site.urls)
    ),
    # my app
    url(
        r'^myapp/', include("djskeletor.myapp.urls")
    ),
    # direct to template
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name="myapp/success.html"
        )
    ),
    # redirect
    url(
        r'^$', RedirectView.as_view(url="/foobar/")
    ),
]
