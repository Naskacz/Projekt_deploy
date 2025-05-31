from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import UserBadge, User
from ..serializers.userbadge_serializers import UserBadgeSerializer
from ..services.badge_service import get_user_badges_service
from rest_framework.generics import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_badges(request,username):
    user = get_object_or_404(User, username=username)
    user_badges = get_user_badges_service(user.id)
    serializer = UserBadgeSerializer(user_badges, many=True)
    return Response(serializer.data)
