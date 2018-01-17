from django.conf.urls import include, url
from django.views.generic import RedirectView, TemplateView

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    # my app
    url(
        r'^billing/', include('djpagan.billing.urls')
    ),
    # redirect
    #url(
    #    r'^$', RedirectView.as_view(url='/foobar/')
    #),
]
