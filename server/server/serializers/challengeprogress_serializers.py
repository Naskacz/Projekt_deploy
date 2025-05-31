from rest_framework import serializers
from ..models import ChallengeProgress
from server.models import ChallengeProgress

class ChallengeProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChallengeProgress
        fields = ['id', 'challenge', 'progress', 'start_date']
        read_only_fields = ['id', 'progress', 'start_date']

    def create(self, validated_data):
        user = self.context['request'].user
        return ChallengeProgress.objects.create(user=user, **validated_data)
