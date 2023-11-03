from django.urls import path, include
from rest_framework.routers import DefaultRouter
from spacehubs.views import ProjectViewSet, NewsViewSet, BlogViewSet, PostViewSet, PodCastViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("news", NewsViewSet, basename="news")
router.register("blogs", BlogViewSet, basename="blog")
router.register("posts", PostViewSet, basename="post")
router.register("podcasts", PodCastViewSet, basename="podcast")

urlpatterns = [
    path("", include(router.urls)),
]
