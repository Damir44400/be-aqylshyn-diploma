from rest_framework.routers import DefaultRouter

from .views import (
    UniversityViewSet,
)

router = DefaultRouter()
router.register(r'', UniversityViewSet, basename='university')

urlpatterns = router.urls
