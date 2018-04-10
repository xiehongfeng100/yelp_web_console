# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Photo(models.Model):
    photo_id = models.CharField(max_length=22)
    business_id = models.CharField(max_length=22)
    caption = models.CharField(max_length=255, default=None)
    label = models.CharField(max_length=255, default=None)
