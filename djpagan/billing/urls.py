from django.conf.urls import url
from django.views.generic import TemplateView

from djpagan.billing import views


urlpatterns = [
    url(
        r'^search/(?P<tipo>[-\w]+)/$',
        views.search, name='search_type'
    ),
]
