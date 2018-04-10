# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import models as custom_models
import serializers as custom_serializers


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = custom_models.Photo.objects.all()
    serializer_class = custom_serializers.PhotoSerializer
    http_method_names = ['get', 'head']
    filter_fields = ('id',)
