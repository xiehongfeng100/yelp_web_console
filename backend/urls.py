# -*- coding: utf-8 -*-
from rest_framework import routers
import views as custom_views

router = routers.DefaultRouter()
router.register(r'photos', custom_views.PhotoViewSet, base_name='photo')

urlpatterns = router.urls
