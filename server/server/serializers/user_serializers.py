from rest_framework import serializers
from ..models import User
class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'join_date', 'followers_count', 'following_count']
    def get_followers_count(self, obj):
        return obj.followers.count()
    def get_following_count(self, obj):
        return obj.following.count()