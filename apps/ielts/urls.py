from rest_framework.routers import DefaultRouter

from apps.ielts import views

router = DefaultRouter()
router.register("modules", views.IeltsViewSet, basename="ielts")

urlpatterns = router.urls
