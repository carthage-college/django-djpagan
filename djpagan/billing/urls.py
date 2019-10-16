from django.urls import path, re_path, reverse_lazy
from django.views.generic import RedirectView

from djpagan.billing import views


urlpatterns = [
    re_path(
        r'^search/(?P<tipo>[-\w]+)/$',
        views.search, name='search_type'
    ),
    path('search/', RedirectView.as_view(url=reverse_lazy('home'))),
]
