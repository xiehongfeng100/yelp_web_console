# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import models as custom_models
import serializers as custom_serializers

from neo4j import Neo4JResource
NEO4J = Neo4JResource()


class RankViewset(viewsets.ReadOnlyModelViewSet):
    queryset = custom_models.Rank.objects.all()
    serializer_class = custom_serializers.RankSerializer

    @action(detail=False)
    def similarities(self, request):
        user = request.query_params['user']
        ret = NEO4J.recommend_by_similarities(user_db_id=user)
        return Response(ret)

    @action(detail=False)
    def friends(self, request):
        user = request.query_params['user']
        ret = NEO4J.recommend_by_friends(user_db_id=user)
        return Response(ret)
