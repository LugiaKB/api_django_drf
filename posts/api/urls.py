from rest_framework.routers import DefaultRouter
from django.urls import path, include

from posts.api.views import PostViewSet

router = DefaultRouter()

router.register('', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]