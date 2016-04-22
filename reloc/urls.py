from django.conf.urls import url
from reloc import views as rlv


urlpatterns = [
    url(r'^restaurants/', rlv.restaurants, name="getrest"),
]