from django.urls import path, include
from .views import (
    RegisterView,
    ActivationView,
    ActivationViewCode,
    LogoutView,
    ChangePasswordView,
    ForgotPasswordView,
    ForgotPasswordCompleteView,
    UsersView,
    # CategoryView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UsersView)
# router.register('category', CategoryView)


urlpatterns = [
    # path('users/', UsersView.as_view({'get': 'list'})),
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('activate/<str:email>/<str:activation_code>/', ActivationView.as_view(), name='activate'),
    path('activate_code/', ActivationViewCode.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('change_password/', ChangePasswordView.as_view()),
    path('lose_password/', ForgotPasswordView.as_view()),
    path('lose_confirm/', ForgotPasswordCompleteView.as_view(), name='forgot'),
]


