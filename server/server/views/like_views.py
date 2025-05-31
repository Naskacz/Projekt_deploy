from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from server.models import Like, Post
from server.serializers.like_serializers import LikeSerializer  # Adjust as per your file

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if created:
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Już polubiono."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_like(request, post_id):
    like = Like.objects.filter(user=request.user, post_id=post_id).first()
    if like:
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Polubienie nie znalezione."}, status=status.HTTP_404_NOT_FOUND)
