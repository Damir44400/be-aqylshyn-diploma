from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from apps.auths import views as auth_views

router = DefaultRouter()
router.register('', auth_views.AuthView, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    path('token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
