# -*- coding: utf-8 -*-
import pandas as pd
from backend.base import models as base_models


YELP_LV_SENTIMENT = pd.read_csv('dataset/las_vegas_review_text_sentiment_with_db_id.csv')


class Utils(object):

    @classmethod
    def get_biz_by_id(cls, db_id):
        qry_result = base_models.Business.objects.filter(id=db_id).first()
        if not qry_result:
            raise base_models.Business.DoesNotExist('Business with id %s does not exist.' % db_id)
        return qry_result

    @classmethod
    def get_biz_name_by_id(cls, db_id):
        qry_result = cls.get_biz_by_id(db_id)
        return qry_result.name

    @classmethod
    def get_biz_reviews_by_id(cls, db_id):
        qry_result = cls.get_biz_by_id(db_id)
        return qry_result.reviews.all()

    @classmethod
    def get_biz_review_ids_by_id(cls, db_id):
        qry_result = cls.get_biz_reviews_by_id(db_id)
        return [result.id for result in qry_result]
