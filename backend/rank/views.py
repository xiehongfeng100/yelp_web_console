# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import models as custom_models
import serializers as custom_serializers

from neo4j import Neo4JUtils
from kdtree import KdTreeUtils
from search import SearchUtils
from utils import Utils, YELP_LV_BIZES


class RankViewset(viewsets.ReadOnlyModelViewSet):
    queryset = custom_models.Rank.objects.all()
    serializer_class = custom_serializers.RankSerializer

    @classmethod
    def _recommend_by_popularity(cls, lat, lon, limit=10):
        """ Recommend businesses by its popularity """
        biz_ids = YELP_LV_BIZES.sort_values('popularity', ascending=False).db_id[:limit].values
        bizes = YELP_LV_BIZES[YELP_LV_BIZES.db_id.isin(biz_ids)]
        return [dict(db_id=db_id,
                     name=Utils.get_biz_name_by_id(db_id),
                     popularity=round(popularity, 2),
                     sentiment=Utils.get_biz_sentiment(db_id),
                     dist=KdTreeUtils.km_between_two_points(lat, lon, lat1, lon1))
                for db_id, popularity, lat1, lon1 in
                zip(bizes.db_id.values, bizes.popularity.values, bizes.latitude.values, bizes.longitude.values)]

    @action(detail=False)
    def similarities(self, request):
        user = request.query_params['user']
        lat = float(request.query_params['lat'])
        lon = float(request.query_params['lon'])
        limit = int(request.query_params.get('limit', 10))
        ret = Neo4JUtils.recommend_by_similarities(user, lat, lon, limit=limit)
        return Response(Utils.sort_by_value(ret, 'recommendation'))

    @action(detail=False)
    def friends(self, request):
        user = request.query_params['user']
        lat = float(request.query_params['lat'])
        lon = float(request.query_params['lon'])
        limit = int(request.query_params.get('limit', 10))
        ret = Neo4JUtils.recommend_by_friends(user, lat, lon, limit=limit)
        return Response(Utils.sort_by_value(ret, 'recommendation'))

    @action(detail=False)
    def popularities(self, request):
        lat = float(request.query_params['lat'])
        lon = float(request.query_params['lon'])
        limit = int(request.query_params.get('limit', 10))
        ret = self._recommend_by_popularity(lat, lon, limit=limit)
        return Response(Utils.sort_by_value(ret, 'popularity'))

    @action(detail=False)
    def dists(self, request):
        lat = float(request.query_params['lat'])
        lon = float(request.query_params['lon'])
        limit = int(request.query_params.get('limit', 10))
        ret = KdTreeUtils.query_closest(lat, lon, limit)
        return Response(Utils.sort_by_value(ret, 'dist'))

    @action(detail=False)
    def search_and_rank(self, request):
        order_by = request.query_params.get('order_by', 'dist')
        keyword = request.query_params['keyword']
        lat = float(request.query_params['lat'])
        lon = float(request.query_params['lon'])
        limit = int(request.query_params.get('limit', 10))

        ret = list()
        if order_by == 'dist':
            ret = SearchUtils.rank_by_distance(keyword, lat, lon, limit=limit)
            ret = Utils.sort_by_value(ret, 'dist', reverse=False)
        elif order_by == 'sentiment':
            ret = SearchUtils.rank_by_sentiment(keyword, lat, lon, limit=limit)
            ret = Utils.sort_by_value(ret, 'sentiment')
        elif order_by == 'popularity':
            ret = SearchUtils.rank_by_popularity(keyword, lat, lon, limit=limit)
            ret = Utils.sort_by_value(ret, 'popularity')
        return Response(ret)
