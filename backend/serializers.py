# -*- coding: utf-8 -*-
from rest_framework import serializers

import models as custom_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = custom_models.User
        fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = custom_models.Friend
        fields = '__all__'


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = custom_models.Business
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = custom_models.Review
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = custom_models.Photo
        fields = '__all__'
