# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from models import Person
from serializers import PersonSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
