from __future__ import unicode_literals
from django.db import models
# Create your models here.


"""
Base Model
"""
class Base(models.Model):
    is_active = models.BooleanField(default=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)


class Chain(Base):
    chain_name = models.CharField(max_length=200, blank=False)


class Restaurant(Base):
    name = models.CharField(max_length=200, blank=False)
    geo = models.CharField(max_length=64, blank=False) #comma-separated latlong will be stored
    is_chain = models.BooleanField(default=False)
    ch = models.ForeignKey(Chain, null=True)


class MenuItem(Base):
    item = models.CharField(max_length=200)
    rt = models.ForeignKey(Restaurant)
    price = models.FloatField()
    prep_time = models.IntegerField()
    is_sensitive = models.IntegerField(default=None, null=True)