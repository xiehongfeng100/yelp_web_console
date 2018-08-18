# -*- coding: utf-8 -*-

from gensim.models import word2vec
from elasticsearch import Elasticsearch
from yelper_web_console import settings
from utils import Utils, YELP_LV_BIZES
from kdtree import KdTreeUtils

# Initialize a global Elastic search instance
ES_INDEX = 'yelp_review'
ES_DOC_TYPE = 'text'
ES = Elasticsearch(settings.ES_HOST + ':' + str(settings.ES_PORT),
                   http_auth=(settings.ES_USERNAME, settings.ES_PASSWORD))

# Load pre-trained word2vec model
W2VMODEL = word2vec.Word2Vec.load('model/yelp_las_vegas_review_text_word_similarities_model')


class SearchUtils(object):

    @classmethod
    def most_similar(cls, word, limit=10):
        # import pdb
        # pdb.set_trace()
        ret = W2VMODEL.wv.most_similar(word, topn=limit)
        return [word_similarity[0] for word_similarity in ret]

    @classmethod
    def _mk_qry_body(cls, keywords, limit=10):
        qry_body = {
            "size": 0,
            "query": {
                "match": {
                    "text_words": ' '.join(keywords)
                }
            },
            "aggs": {
                "by_biz": {
                    "terms": {
                        "field": "business_db_id",
                        "size": limit
                    }
                }
            }
        }
        return qry_body

    @classmethod
    def _search(cls, keyword, limit=10):
        similar_words = cls.most_similar(keyword)
        similar_words.append(keyword)  # keyword should be included
        qry_body = cls._mk_qry_body(similar_words, limit=limit)
        result = ES.search(index=ES_INDEX, doc_type=ES_DOC_TYPE, body=qry_body)
        return [biz['key'] for biz in result['aggregations']['by_biz']['buckets']]

    @classmethod
    def _rank(cls, keyword, lat, lon, limit=10, order_by='dist'):
        bizes = cls._search(keyword, limit=limit)
        bizes = YELP_LV_BIZES[YELP_LV_BIZES.db_id.isin(bizes)]
        ret = [dict(db_id=db_id,
                    name=Utils.get_biz_name_by_id(db_id),
                    popularity=round(popularity, 2),
                    sentiment=Utils.get_biz_sentiment(db_id),
                    dist=KdTreeUtils.km_between_two_points(lat, lon, lat1, lon1))
               for db_id, popularity, lat1, lon1 in
               zip(bizes.db_id.values, bizes.popularity.values, bizes.latitude.values, bizes.longitude.values)]
        return sorted(ret, key=lambda item: item[order_by], reverse=True)

    @classmethod
    def rank_by_distance(cls, keyword, lat, lon, limit=10):
        """ Rank businesses by its distance to user """
        return cls._rank(keyword, lat, lon, limit=limit, order_by='dist')

    @classmethod
    def rank_by_sentiment(cls, keyword, lat, lon, limit=10):
        """ Rank businesses by its mean review text (cnn) sentiment """
        return cls._rank(keyword, lat, lon, limit=limit, order_by='sentiment')

    @classmethod
    def rank_by_popularity(cls, keyword, lat, lon, limit=10):
        """ Rank businesses by its popularity """
        return cls._rank(keyword, lat, lon, limit=limit, order_by='popularity')
