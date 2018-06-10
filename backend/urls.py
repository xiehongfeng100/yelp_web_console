# -*- coding: utf-8 -*-
from rest_framework import routers
import views as custom_views

router = routers.DefaultRouter()
router.register(r'users', custom_views.UserViewSet, base_name='user')
router.register(r'friends', custom_views.FriendViewSet, base_name='friend')
router.register(r'businesses', custom_views.BusinessViewSet, base_name='business')
router.register(r'reviews', custom_views.ReviewViewSet, base_name='review')
router.register(r'photos', custom_views.PhotoViewSet, base_name='photo')


urlpatterns = router.urls
