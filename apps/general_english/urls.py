from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.general_english.views import module
from apps.general_english.views import trial_test

router = DefaultRouter()
router.register('trial-tests', trial_test.TrialTestViewSet, basename='trial-test')
router.register('modules', module.ModuleViewSet, basename='modules')

urlpatterns = [
    path('', include(router.urls))
]
