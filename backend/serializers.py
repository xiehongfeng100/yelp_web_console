# -*- coding: utf-8 -*-
from rest_framework import serializers

import models as custom_models


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = custom_models.Photo
        fields = '__all__'
