from rest_framework import serializers
from ..models import User
from ..services.user_service import get_user_by_username

class FollowSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Użytkownik o takiej nazwie nie istnieje")
        return value