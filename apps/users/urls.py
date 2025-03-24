from rest_framework.routers import DefaultRouter

from apps.users import views as user_views

router = DefaultRouter()

router.register('', user_views.UserViewSet, basename='user')

urlpatterns = router.urls
