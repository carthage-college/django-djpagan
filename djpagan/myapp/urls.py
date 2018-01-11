from django.conf.urls import url
from django.views.generic import TemplateView

from djskeletor.myapp import views

urlpatterns = [
    url(
        r'^myview/(?P<pid>\d+)/$',
        views.myview, name='myapp_display'
    ),
    url(
        r'^myview/$',
        views.myview, name='myapp_display_no_pid'
    ),
    url(
        r'^search/$',
        views.search, name='myapp_search'
    ),
    url(
        r'^myview/success/$',
        TemplateView.as_view(
            template_name='myapp/success.html'
        ),
        name='myapp_success'
    ),
)
