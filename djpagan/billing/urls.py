from django.conf.urls import url
from django.views.generic import TemplateView

from djpagan.billing import views


urlpatterns = [
    url(
        r'^search/$',
        views.search, name='search_home'
    ),
    url(
        r'^search/(?P<tipo>\d+)/$',
        views.search, name='search_type'
    ),
]
