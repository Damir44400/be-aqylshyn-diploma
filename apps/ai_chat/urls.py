from rest_framework.routers import DefaultRouter
from apps.ai_chat.views import ChatViewSet

router = DefaultRouter()
router.register(r'', ChatViewSet, basename='chat')

urlpatterns = router.urls
