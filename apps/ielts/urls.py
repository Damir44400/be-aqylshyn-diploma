from rest_framework.routers import DefaultRouter

from apps.ielts import views

router = DefaultRouter()
router.register("modules", views.IeltsViewSet, basename="ielts")
router.register(r"modules/tests", views.IeltsTestSubmitViewSet, basename="ielts-test-submit")

urlpatterns = router.urls
