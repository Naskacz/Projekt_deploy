from rest_framework import serializers
from ..models import UserBadge
from .badge_serializers import BadgeSerializer

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer()

    class Meta:
        model = UserBadge
        fields = ['id', 'badge', 'awarded_date']