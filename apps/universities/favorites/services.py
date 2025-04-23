from apps.universities.favorites import models as favorites_models


class FavoriteService:
    def insert_favorite(self, university, user):
        favorite = favorites_models.Favorite.objects.filter(university=university, user=user).first()
        if not favorite:
            favorites_models.Favorite.objects.create(university=university, user=user)
        else:
            favorite.delete()
