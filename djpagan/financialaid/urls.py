from django.conf.urls import url
from django.views.generic import TemplateView

from djpagan.financialaid import views


urlpatterns = [
    url(
        r'^wisact284/$', views.wisact284, name='wisact284'
    ),
]
