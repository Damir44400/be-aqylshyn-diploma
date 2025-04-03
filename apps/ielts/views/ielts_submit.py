from rest_framework import viewsets

from apps.common import mixins as common_mixins


class IeltsSubmitView(
    common_mixins.ActionSerializerMixin,
    viewsets.GenericViewSet
):
    serializers = {
        ""
    }


    def submit(self, ):