# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import models as custom_models
import serializers as custom_serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = custom_models.User.objects.all()
    serializer_class = custom_serializers.UserSerializer
    http_method_names = ['get', 'head']
    filter_fields = ()


class FriendViewSet(viewsets.ModelViewSet):
    queryset = custom_models.Friend.objects.all()
    serializer_class = custom_serializers.FriendSerializer
    http_method_names = ['get', 'head']
    filter_fields = ()


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = custom_models.Business.objects.all()
    serializer_class = custom_serializers.BusinessSerializer
    http_method_names = ['get', 'head']
    filter_fields = ()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = custom_models.Review.objects.all()
    serializer_class = custom_serializers.ReviewSerializer
    http_method_names = ['get', 'head']
    filter_fields = ()


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = custom_models.Photo.objects.all()
    serializer_class = custom_serializers.PhotoSerializer
    http_method_names = ['get', 'head']
    filter_fields = ('id',)
