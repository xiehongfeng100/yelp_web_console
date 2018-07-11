# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import models as custom_models
import serializers as custom_serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = custom_models.User.objects.all()
    serializer_class = custom_serializers.UserSerializer
    filter_fields = ()


class FriendViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = custom_models.Friend.objects.all()
    serializer_class = custom_serializers.FriendSerializer
    filter_fields = ()


class BusinessViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = custom_models.Business.objects.all()
    serializer_class = custom_serializers.BusinessSerializer
    filter_fields = ()


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = custom_models.Review.objects.all()
    serializer_class = custom_serializers.ReviewSerializer
    filter_fields = ()


class CheckInViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = custom_models.CheckIn.objects.all()
    serializer_class = custom_serializers.CheckInSerializer
    filter_fields = ()


class PhotoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = custom_models.Photo.objects.all()
    serializer_class = custom_serializers.PhotoSerializer
    filter_fields = ()
