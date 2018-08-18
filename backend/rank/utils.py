# -*- coding: utf-8 -*-
import pandas as pd
from backend.base import models as base_models

YELP_LV_BIZES = pd.read_csv('dataset/las_vegas_businesses.csv')


class Utils(object):

    @classmethod
    def get_biz_by_id(cls, db_id):
        qry_result = base_models.Business.objects.get(pk=db_id)  # Raise on not found
        return qry_result

    @classmethod
    def get_biz_name_by_id(cls, db_id):
        qry_result = cls.get_biz_by_id(db_id)
        return qry_result.name

    @classmethod
    def get_biz_sentiment(cls, db_id):
        return round(YELP_LV_BIZES[YELP_LV_BIZES.db_id == db_id].sentiment.values[0], 2)

    @classmethod
    def scale(cls, value, value_range=(0.0, 5.0), feature_range=(0.0, 1.0)):
        # TODO. assert value_range[0] != value_range[1]
        std = float(value - value_range[0]) / (value_range[1] - value_range[0])
        return std * (feature_range[1] - feature_range[0]) + feature_range[0]

    @classmethod
    def sort_by_value(cls, value, key, reverse=True):
        # TODO. assert value is a list of dicts
        return sorted(value, key=lambda item: item[key], reverse=reverse)
