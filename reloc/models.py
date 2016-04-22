from django.db import models
from __future__ import unicode_literals
# Create your models here.


"""
Base Model
"""
class Base(models.Model):
    is_active = models.BooleanField(default=True)
    modified_on = models.DatetimeField(auto_now=True)
    created_on = models.DatetimeField(auto_now_add=True)


class Restaurant(Base):
    name = models.CharField(max_length=200)
    geo = models.CharField(max_length=64) #comma-separated latlong will be stored
    is_branch = models.BooleanField(default=True)
    is_chain = models.BooleanField(default=False)


class MenuItem(Base):
    item = models.CharField(max_length=200)
    price = models.FloatField()
    prep_time = models.IntegerField()
    is_sensitive = models.BooleanField(default=False)