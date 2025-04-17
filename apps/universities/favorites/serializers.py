from rest_framework import serializers

from .models import Favorite
from ..serializers import UniversityListSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    university = UniversityListSerializer(many=False)

    class Meta:
        model = Favorite
        fields = ('id', 'university', 'created_at')


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('university',)
