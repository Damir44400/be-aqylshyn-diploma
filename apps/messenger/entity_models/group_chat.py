from django.db import models

from apps.common import models as common_models
from apps.users import models as user_models


class GroupChat(common_models.BaseModel):
    name = models.CharField(max_length=120)
    sender = models.OneToOneField(user_models.User, on_delete=models.CASCADE)
    members = models.ManyToManyField(user_models.User, related_name='group_chats')
