from django.conf.urls import url
from reloc import views as rlv


url_patterns = [
    url(r'^restaurants/', rlv.restaurants, name="getrest"),
]