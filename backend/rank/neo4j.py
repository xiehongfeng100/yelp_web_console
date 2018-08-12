# -*- coding: utf-8 -*-
import numpy as np
from py2neo import Graph
from yelper_web_console import settings
from kdtree import YELP_LV_BIZES
from utils import YELP_LV_SENTIMENT
from kdtree import KDTreeUtil
from utils import Utils


class Neo4JResource(object):
    def __init__(self):
        self.graph = Graph(auth=(settings.NEO_USERNAME, settings.NEO_PASSWORD))
        self.kdtree = KDTreeUtil()

    @classmethod
    def scaler(cls, value, value_range=(0.0, 5.0), feature_range=(0.0, 1.0)):
        # TODO. assert value_range[0] != value_range[1]
        std = float(value - value_range[0]) / (value_range[1] - value_range[0])
        return std * (feature_range[1] - feature_range[0]) + feature_range[0]

    def _dist_between_two_points(self, lat0, lon0, lat1, lon1):
        x0, y0, z0 = self.kdtree.to_Cartesian(lat0, lon0)
        x1, y1, z1 = self.kdtree.to_Cartesian(lat1, lon1)
        return self.kdtree.distToKM(np.sqrt(np.power(x0-x1, 2) + np.power(y0-y1, 2) + np.power(z0-z1, 2)))

    def _calc_biz_sentiment(self, db_id):
        reviews = Utils.get_biz_review_ids_by_id(db_id)
        return YELP_LV_SENTIMENT[YELP_LV_SENTIMENT.review_db_id.isin(reviews)].cnn_sentiment.mean()

    def recommend_by_similarities(self, user_db_id, lat, lon, limit=10):
        """ Recommend businesses from other users through similarities """
        qry_str = '''
            MATCH (u1:USER)-[r:REVIEW]->(biz:BUSINESS), (u1)-[s:SIMILARITY]-(u2:USER {db_id: %s})
            WHERE NOT((u2)-[:REVIEW]->(biz))
            WITH biz, s.similarity AS similarity, r.stars_time_scaled AS stars
            ORDER BY biz.db_id, similarity DESC
            WITH biz.db_id AS db_id, COLLECT(stars)[0..3] AS starses
            WITH db_id, REDUCE(s = 0, i IN starses | s + i)*1.0 / LENGTH(starses) AS recommendation
            ORDER BY recommendation DESC
            RETURN db_id, recommendation LIMIT %s
        ''' % (user_db_id, limit)
        qry_result = self.graph.run(qry_str)
        data = [record.data() for record in qry_result]
        id_data_maps = {item['db_id']: item for item in data}
        bizes = YELP_LV_BIZES[YELP_LV_BIZES.db_id.isin(id_data_maps.keys())]
        return [dict(db_id=db_id,
                     name=Utils.get_biz_name_by_id(db_id),
                     popularity=popularity,
                     sentiment=self._calc_biz_sentiment(db_id),
                     dist=self._dist_between_two_points(lat, lon, lat1, lon1),
                     recommendation=self.scaler(id_data_maps[db_id]['recommendation']))
                for db_id, popularity, lat1, lon1 in
                zip(bizes.db_id.values, bizes.popularity.values, bizes.latitude.values, bizes.longitude.values)]

    def recommend_by_friends(self, user_db_id, lat, lon, limit=10):
        """ Recommend businesses from friends """
        qry_str = '''
            MATCH (u1:USER)-[r:REVIEW]->(biz:BUSINESS), (u1)-[f:FRIEND]-(u2:USER {db_id: %s})
            WHERE NOT ((u2)-[:REVIEW]->(biz))
            WITH biz, r.stars_time_scaled AS stars
            ORDER BY biz.db_id, stars DESC
            WITH biz.db_id AS db_id, COLLECT(stars)[0..3] AS starses
            WITH db_id, REDUCE(s = 0, i IN starses | s + i)*1.0 / LENGTH(starses) AS recommendation
            ORDER BY recommendation DESC
            RETURN db_id , recommendation LIMIT %s
        ''' % (user_db_id, limit)
        qry_result = self.graph.run(qry_str)
        data = [record.data() for record in qry_result]
        id_data_maps = {item['db_id']: item for item in data}
        bizes = YELP_LV_BIZES[YELP_LV_BIZES.db_id.isin(id_data_maps.keys())]
        return [dict(db_id=db_id,
                     name=Utils.get_biz_name_by_id(db_id),
                     popularity=popularity,
                     sentiment=self._calc_biz_sentiment(db_id),
                     dist=self._dist_between_two_points(lat, lon, lat1, lon1),
                     recommendation=self.scaler(id_data_maps[db_id]['recommendation']))
                for db_id, popularity, lat1, lon1 in
                zip(bizes.db_id.values, bizes.popularity.values, bizes.latitude.values, bizes.longitude.values)]

    def recommend_by_popularity(self):
        """ Recommend businesses by its popularity """
        pass
