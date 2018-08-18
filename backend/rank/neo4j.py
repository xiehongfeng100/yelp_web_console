# -*- coding: utf-8 -*-
from py2neo import Graph
from yelper_web_console import settings

from utils import Utils
from kdtree import KdTreeUtils
from kdtree import YELP_LV_BIZES

# Initialize a global Graph instance
GRAPH = Graph(host=settings.NEO_HOST, port=settings.NEO_PORT,
              auth=(settings.NEO_USERNAME, settings.NEO_PASSWORD))


class Neo4JUtils(object):

    @classmethod
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
        qry_result = GRAPH.run(qry_str)
        data = [record.data() for record in qry_result]
        id_data_maps = {item['db_id']: item for item in data}
        bizes = YELP_LV_BIZES[YELP_LV_BIZES.db_id.isin(id_data_maps.keys())]
        return [dict(db_id=db_id,
                     name=Utils.get_biz_name_by_id(db_id),
                     popularity=round(popularity, 2),
                     sentiment=Utils.get_biz_sentiment(db_id),
                     dist=KdTreeUtils.km_between_two_points(lat, lon, lat1, lon1),
                     recommendation=Utils.scale(id_data_maps[db_id]['recommendation']))
                for db_id, popularity, lat1, lon1 in
                zip(bizes.db_id.values, bizes.popularity.values, bizes.latitude.values, bizes.longitude.values)]

    @classmethod
    def recommend_by_friends(cls, user_db_id, lat, lon, limit=10):
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
        qry_result = GRAPH.run(qry_str)
        data = [record.data() for record in qry_result]
        id_data_maps = {item['db_id']: item for item in data}
        bizes = YELP_LV_BIZES[YELP_LV_BIZES.db_id.isin(id_data_maps.keys())]
        return [dict(db_id=db_id,
                     name=Utils.get_biz_name_by_id(db_id),
                     popularity=round(popularity, 2),
                     sentiment=Utils.get_biz_sentiment(db_id),
                     dist=KdTreeUtils.km_between_two_points(lat, lon, lat1, lon1),
                     recommendation=Utils.scale(id_data_maps[db_id]['recommendation']))
                for db_id, popularity, lat1, lon1 in
                zip(bizes.db_id.values, bizes.popularity.values, bizes.latitude.values, bizes.longitude.values)]
