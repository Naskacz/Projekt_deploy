from rest_framework import serializers
from server.models import Challenge

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Challenge
        fields = ['id', 'name', 'description', 'type', 'frequency', 'duration', 'is_public', 'create_date']
        read_only_fields = ['id', 'creator', 'create_date']