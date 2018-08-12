# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import models as custom_models
import serializers as custom_serializers

from neo4j import Neo4JResource
from kdtree import KDTreeUtil

NEO4J = Neo4JResource()
KDTREEUTIL = KDTreeUtil()


class RankViewset(viewsets.ReadOnlyModelViewSet):
    queryset = custom_models.Rank.objects.all()
    serializer_class = custom_serializers.RankSerializer

    @action(detail=False)
    def similarities(self, request):
        user = request.query_params['user']
        lat = float(request.query_params['lat'])
        lon = float(request.query_params['lon'])
        limit = int(request.query_params.get('limit', 10))
        ret = NEO4J.recommend_by_similarities(user, lat, lon, limit=limit)
        return Response(ret)

    @action(detail=False)
    def friends(self, request):
        user = request.query_params['user']
        lat = float(request.query_params['lat'])
        lon = float(request.query_params['lon'])
        limit = int(request.query_params.get('limit', 10))
        ret = NEO4J.recommend_by_friends(user, lat, lon, limit=limit)
        return Response(ret)

    @action(detail=False)
    def dists(self, request):
        lat = float(request.query_params['lat'])
        lon = float(request.query_params['lon'])
        limit = int(request.query_params.get('limit', 10))
        ret = KDTREEUTIL.query_closest(lat, lon, limit)
        return Response(ret)
