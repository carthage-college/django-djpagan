from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from djpagan.billing import views


urlpatterns = [
    url(
        r'^search/(?P<tipo>[-\w]+)/$',
        views.search, name='search_type'
    ),
    url(
        r'^search/$',
        RedirectView.as_view(url=reverse_lazy('home'))
    ),
]
