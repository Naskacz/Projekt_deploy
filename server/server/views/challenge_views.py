from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..serializers.challenge_serializers import ChallengeSerializer
from ..models import Challenge
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_challenge(request):
    serializer = ChallengeSerializer(data=request.data)
    if serializer.is_valid():
        challenge = serializer.save(creator=request.user)
        return Response({"message": "Wyzwanie utworzone!",
                         "challenge_id": challenge.id,
                         "title": challenge.name}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_challenges(request):
    challenges = Challenge.objects.all()
    serializer = ChallengeSerializer(challenges, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_challenges(request):
    challenges = Challenge.objects.filter(creator=request.user).order_by('name')
    serializer = ChallengeSerializer(challenges, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_praticipate_challenges(request):
    challenges = Challenge.objects.filter(
    challengeprogress__user=request.user
    ).distinct().order_by('name')
    serializer = ChallengeSerializer(challenges, many=True)
    return Response(serializer.data)
