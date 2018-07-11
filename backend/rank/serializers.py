# -*- coding: utf-8 -*-
from rest_framework import serializers

import models as custom_models


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = custom_models.Rank
        fields = '__all__'
