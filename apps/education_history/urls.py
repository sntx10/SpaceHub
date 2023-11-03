from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EducationHistoryViewSet, LanguageViewSet

routers = DefaultRouter()
routers.register('education_history', EducationHistoryViewSet)
routers.register('add_language', LanguageViewSet)

urlpatterns = [
    path('', include(routers.urls))
]
