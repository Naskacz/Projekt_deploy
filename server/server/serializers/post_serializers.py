from rest_framework import serializers
from ..models import Post, UserBadge

class PostSerializer(serializers.ModelSerializer):
    comment_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'creator', 'name', 'description', 'user_badge', 'comment_count', 'like_count']
        read_only_fields = ['id', 'creator', 'comment_count', 'like_count']

    def validate_user_badge(self, badge):
        user = self.context['request'].user
        if badge and badge.user != user:
            raise serializers.ValidationError("You can only use your own badges.")
        return badge

    def create(self, validated_data):
        user = self.context['request'].user
        return Post.objects.create(creator=user, **validated_data)
