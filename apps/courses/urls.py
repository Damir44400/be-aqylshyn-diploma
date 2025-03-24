from rest_framework.routers import DefaultRouter

from apps.courses import views

router = DefaultRouter()
router.register('courses', views.CourseViewSet, basename='courses')


urlpatterns = router.urls