from django.conf.urls import url
from reloc import views as rlv


urlpatterns = [
    url(r'^resla/', rlv.rest_sla, name="getresla"),
]