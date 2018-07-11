# -*- coding: utf-8 -*-
from py2neo import Graph
from yelper_web_console import settings


class Neo4JResource(object):
    def __init__(self):
        self.graph = Graph(auth=(settings.NEO_USERNAME, settings.NEO_PASSWORD))

    @classmethod
    def scaler(cls, value, value_range=(0.0, 5.0), feature_range=(0.0, 1.0)):
        # TODO. assert value_range[0] != value_range[1]
        std = float(value - value_range[0]) / (value_range[1] - value_range[0])
        return std * (feature_range[1] - feature_range[0]) + feature_range[0]

    def recommend_by_similarities(self, user_db_id):
        """ Recommend businesses from other users through similarities """
        qry_str = '''
            MATCH (u1:USER)-[r:REVIEW]->(b:BUSINESS), (u1)-[s:SIMILARITY]-(u2:USER {db_id: %s})
            WHERE NOT((u2)-[:REVIEW]->(b))
            WITH b, s.similarity AS similarity, r.stars AS stars
            ORDER BY b.business_id, similarity DESC
            WITH b.business_id AS business, COLLECT(stars)[0..3] AS starses
            WITH business, REDUCE(s = 0, i IN starses | s + i)*1.0 / LENGTH(starses) AS recommendation
            ORDER BY recommendation DESC
            RETURN business, recommendation
        ''' % user_db_id
        results = list()
        for record in self.graph.run(qry_str):
            data = record.data()
            data['recommendation'] = self.scaler(data['recommendation'])
            results.append(data)
        return results

    def recommend_by_friends(self, user_db_id):
        """ Recommend businesses from friends """
        qry_str = '''
            MATCH (u1:USER)-[r:REVIEW]->(b:BUSINESS), (u1)-[f:FRIEND]-(u2:USER {db_id: %s})
            WHERE NOT((u2)-[:REVIEW]->(b))
            WITH b, r.stars AS stars
            WITH b.business_id AS business, COLLECT(stars)[0..3] AS starses
            WITH business, REDUCE(s = 0, i IN starses | s + i)*1.0 / LENGTH(starses) AS recommendation
            ORDER BY recommendation DESC
            RETURN business , recommendation
        ''' % user_db_id
        results = list()
        for record in self.graph.run(qry_str):
            data = record.data()
            data['recommendation'] = self.scaler(data['recommendation'])
            results.append(data)
        return results

    def recommend_by_popularity(self):
        """ Recommend businesses by its popularity """
        pass
