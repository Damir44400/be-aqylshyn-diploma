from rest_framework.routers import DefaultRouter

from apps.ielts.views import ielts_module
from apps.ielts.views import ielts_sub_module
from apps.ielts.views import ielts_test

router = DefaultRouter()
router.register("modules", ielts_module.IeltsView, basename="module")
router.register("submodules", ielts_sub_module.IeltsSubModuleView, basename="module-sub-module")
router.register("tests", ielts_test.IeltsTestViewSet, basename="module-sub-module-test")

urlpatterns = router.urls
