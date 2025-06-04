from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..serializers.auth_serializers import PasswordResetSerializer, User, CustomTokenObtainPairSerializer
from ..serializers.follow_serializers import FollowSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.exceptions import ValidationError
from ..services.follow_service import follow_user_service, get_following_service, get_followers_service, unfollow_user_service
from ..services.user_service import sign_up_service, get_user_by_username
from ..serializers.user_serializers import UserProfileSerializer
from ..services.challenge_service import get_common_challenges
from ..serializers.challenge_serializers import ChallengeSerializer
class CustomTokenObtainPairView(TokenViewBase):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
def get_user(request):
    data = list(User.objects.values())
    return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    try:
        user = sign_up_service(request.data)
        return Response({"message":"Zarejestrowano pomyślnie",
                         "user_id": user.id,
                         "email":user.email},status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response(e.detail,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_password(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        response_data = {
            "message": "Hasło zostało zresetowane.",
            "user_id": user.id,
            "email": user.email
        }
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request):
    serializer = FollowSerializer(data=request.data)
    if serializer.is_valid():
        user_to_follow_username = serializer.validated_data['username']
        result = follow_user_service(request.user, user_to_follow_username)
        return Response(result, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request, username):
    serializer = FollowSerializer(data={'username': username})
    if serializer.is_valid():
        followers_data = get_followers_service(username)
        return Response(followers_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request, username):
    serializer = FollowSerializer(data={'username': username})
    if serializer.is_valid():
        following_data = get_following_service(username)
        return Response(following_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request):
    serializer = FollowSerializer(data=request.data)
    if serializer.is_valid():
        result = unfollow_user_service(request.user, serializer.validated_data['username'])
        return Response({"message":result}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_userprofile_data(request, username):
    user = get_user_by_username(username)
    common_challenges = get_common_challenges(request.user, user)
    challenges_serializer = ChallengeSerializer(common_challenges, many=True)
    profile_serializer = UserProfileSerializer(user)
    return Response({
        'profile': profile_serializer.data,
        'common_challenges': challenges_serializer.data })
