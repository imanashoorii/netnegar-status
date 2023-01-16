from rest_framework import serializers
from .models import User
from .utils import toJalaliDateTime


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'first_name', 'last_name', 'date_joined']

    def to_representation(self, instance: User):
        return {
            "id": instance.id,
            "isAdmin": instance.is_superuser,
            "name": instance.get_full_name(),
            "updatedAt": toJalaliDateTime(instance.updatedAt)
        }
