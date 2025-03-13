from rest_framework import permissions


class ActionSerializerMixin:
    serializers = {}

    def get_serializer_class(self):
        """Return serializer class based on action."""
        if self.action in self.serializers:
            return self.serializers[self.action]

        return super().get_serializer_class()


class ActionPermissionMixin:
    DEFAULT_PERMISSION_CLASS = permissions.IsAuthenticated
    permissions = {}

    def get_permissions(self):
        if self.action in self.permissions:
            return [
                permission()
                for permission in self.permissions[self.action]
            ]

        return [self.DEFAULT_PERMISSION_CLASS()]
