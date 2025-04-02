from django.db import models

from apps.common import models as common_models
from apps.users import models as user_models


class Chat(models.Model, common_models.BaseModel):
    sender = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(user_models.User, on_delete=models.CASCADE)
    message = models.TextField()
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
