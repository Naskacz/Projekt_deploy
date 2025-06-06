from rest_framework import serializers
from server.models import Badge

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'type', 'challenge']