from django.urls import path, include
# from .views import ProfileCreate, CountryViewSet
from rest_framework.routers import DefaultRouter
from .views import RomProfileViewSet, ToggleSubscriptionAPIView, SubscriptionsListView, FollowersListView

routers = DefaultRouter()
# routers.register('profile', ProfileCreate)
# routers.register('country', CountryViewSet)
# routers.register('profile', ProfileViewSet)
routers.register('profile', RomProfileViewSet)

urlpatterns = [
    path('toggle-subscription/<int:user_id>/', ToggleSubscriptionAPIView.as_view(), name='toggle_subscription'),
    path('subscriptions/', SubscriptionsListView.as_view(), name='subscriptions_list'),
    path('followers/', FollowersListView.as_view(), name='followers_list'),
    path('', include(routers.urls)),

    # path('profile/', ProfileCreate.as_view())
]
