from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models import Challenge, ChallengeProgress
from ..serializers.challengeprogress_serializers import ChallengeProgressSerializer  # popraw, jeśli masz inną ścieżkę
from ..services.badge_service import award_badges_for_progress

from django.utils import timezone
from datetime import timedelta
import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_challenge_progress(request):
    serializer = ChallengeProgressSerializer(data=request.data)
    if serializer.is_valid():
        challenge = serializer.validated_data['challenge']

        # Sprawdzenie czy user już ma progress dla tego challenge
        if ChallengeProgress.objects.filter(user=request.user, challenge=challenge).exists():
            return Response({"error": "Już masz postęp dla tego wyzwania."}, status=status.HTTP_400_BAD_REQUEST)

        challenge_progress = ChallengeProgress.objects.create(
            user=request.user,
            challenge=challenge
        )
        result_serializer = ChallengeProgressSerializer(challenge_progress)
        return Response(result_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def increment_progress(request):
    progress_id = request.data.get('progress_id')
    if not progress_id:
        return Response({'error': 'Brakuje progress_id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        progress = ChallengeProgress.objects.get(id=progress_id, user=request.user)
    except ChallengeProgress.DoesNotExist:
        return Response({'error': 'Nie znaleziono postępu'}, status=status.HTTP_404_NOT_FOUND)

    now = timezone.now().date()
    last = progress.last_updated
    freq = progress.challenge.frequency
    days_since_last = (now - last).days
    if days_since_last < freq:
        return Response({'error': f'Postęp można aktualizować co {freq} dni. Pozostało {freq - days_since_last} dni.'},
                        status=status.HTTP_400_BAD_REQUEST)
    # Wyliczenie streak:  
    if (now - last).days == freq:
        progress.streak += freq
    else:
        progress.streak = 1

    progress.progress += 1
    progress.last_updated = now
    if(progress.percent_complete >= 100):
        progress.is_active = False
    progress.save()

    # → przypisz badge’y
    award_badges_for_progress(progress)

    return Response({
        'success': True,
        'updated_progress': progress.progress,
        'streak': progress.streak,
        'percent_complete': progress.percent_complete,
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def activate_or_deactivate_challenge(request):
    progress_id = request.data.get('progress_id')
    if not progress_id:
        return Response({'error': 'Brakuje progress_id'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        progress = ChallengeProgress.objects.get(id=progress_id, user=request.user)
    except ChallengeProgress.DoesNotExist:
        return Response({'error': 'Nie znaleziono postępu'}, status=status.HTTP_404_NOT_FOUND)

    progress.is_active = not progress.is_active
    progress.save()

    return Response({
        'success': True,
        'is_active': progress.is_active,
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user_challenge_progresses(request):
    user = request.user
    progresses = ChallengeProgress.objects.filter(user=user)
    serializer = ChallengeProgressSerializer(progresses, many=True)
    return Response(serializer.data)