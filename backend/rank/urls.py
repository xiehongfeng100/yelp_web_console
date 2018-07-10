# -*- coding: utf-8 -*-
from rest_framework import routers
import views as custom_views

router = routers.DefaultRouter()
# router.register(r'ranks', custom_views.RankViewset, base_name='rank')

urlpatterns = router.urls
