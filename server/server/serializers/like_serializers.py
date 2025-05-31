from rest_framework import serializers
from server.models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post']
        read_only_fields = ['user']