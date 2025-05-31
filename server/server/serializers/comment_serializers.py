from rest_framework import serializers
from server.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'creator', 'post', 'description', 'create_date']
        read_only_fields = ['creator', 'create_date']