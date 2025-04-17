from rest_framework.routers import DefaultRouter

from .views import (
    UniversityViewSet,
)
from .favorites.views import FavoriteViewSet

router = DefaultRouter()
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'', UniversityViewSet, basename='university')
urlpatterns = router.urls
