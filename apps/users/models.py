from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common import models as common_models
from apps.users import managers as user_managers


class User(AbstractUser, common_models.BaseModel):
    username = None
    profile_picture = models.ImageField(upload_to="profile_picture", null=True, blank=True)
    first_name = models.CharField(max_length=30, verbose_name=_("First Name"))
    email = models.EmailField(unique=True, verbose_name=_("Email"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]
    objects = user_managers.UserManager()

    class Meta:
        verbose_name = _("Қолданушы")
        verbose_name_plural = _("Қолданушылар тізімі")
