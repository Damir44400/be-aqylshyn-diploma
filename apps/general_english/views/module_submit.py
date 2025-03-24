from rest_framework import generics

from apps.common import mixins as common_mixins


class ModuleSubmitsView(
    common_mixins.ActionSerializerMixin,
    generics.GenericAPIView
):
    serializers = {}
