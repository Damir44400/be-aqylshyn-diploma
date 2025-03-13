from rest_framework import generics

from src.common import mixins as common_mixins
from src.users import models as user_models


# Create your views here.
class UserViewSet(
    common_mixins.ActionSerializerMixin,
    common_mixins.ActionPermissionMixin,
    generics.GenericAPIView
):
    queryset = user_models.User.objects.all()
    serializers = {
        ""
    }
