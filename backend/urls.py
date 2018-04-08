# -*- coding: utf-8 -*-
from rest_framework import routers
from views import PersonViewSet

router = routers.DefaultRouter()
router.register(r'persons', PersonViewSet, base_name='person')

urlpatterns = router.urls
