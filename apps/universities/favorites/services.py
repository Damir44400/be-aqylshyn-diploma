from rest_framework.exceptions import ValidationError

from apps.universities import models
from apps.universities.favorites import models as favorites_models


class FavoriteService:
    def insert_favorite(self, university_id, user):
        university = models.University.objects.filter(id=university_id).first()
        if not university:
            raise ValidationError("No such university")

        favorite = favorites_models.Favorite.objects.filter(university=university, user=user).first()
        if not favorite:
            favorites_models.Favorite.objects.create(university=university, user=user)
        else:
            favorite.delete()
