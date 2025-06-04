from django.db import transaction
from ..models import Badge, UserBadge, ChallengeProgress, Notification

def get_user_badges_service(user):
    """
    Zwraca queryset UserBadge dla danego usera.
    """
    return UserBadge.objects.filter(user=user).select_related('badge', 'badge__challenge')

def award_badges_for_progress(progress: ChallengeProgress):
    """
    Po każdej aktualizacji progress:
    - liczymy percent_complete i streak
    - przyznajemy badge’y za 50%, 100%, 7-dniowy i 30-dniowy streak
    """
    user = progress.user
    challenge = progress.challenge
    pct = progress.percent_complete
    streak = progress.streak

    with transaction.atomic():
        # 50% badge
        if pct >= 50:
            try:
                badge = Badge.objects.get(type='halfway_there', challenge=challenge)
                created, _ = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    notif = Notification.objects.create(user=user, message=f"Gratulacje! Zdobyłeś odznakę: {badge.type}, {badge.challenge.name}", notification_type='badge_awarded')
            except Badge.DoesNotExist:
                pass


        # 100% badge
        if pct >= 100:
            try:
                badge = Badge.objects.get(type='complete_challenge', challenge=challenge)
                created, _ = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    notif = Notification.objects.create(user=user, message=f"Gratulacje! Zdobyłeś odznakę: {badge.type}, {badge.challenge.name}", notification_type='badge_awarded')
            except Badge.DoesNotExist:
                pass


        # 7-dniowy streak
        if streak >= 7:
            try:
                badge = Badge.objects.get(type='streak_7_days', challenge=challenge)
                created, _ = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    notif = Notification.objects.create(user=user, message=f"Gratulacje! Zdobyłeś odznakę: {badge.type}, {badge.challenge.name}", notification_type='badge_awarded')
            except Badge.DoesNotExist:
                pass


        # 30-dniowy streak
        if streak >= 30:
            try:
                badge = Badge.objects.get(type='streak_30_days', challenge=challenge)
                created, _ = UserBadge.objects.get_or_create(user=user, badge=badge)
                if created:
                    notif = Notification.objects.create(user=user, message=f"Gratulacje! Zdobyłeś odznakę: {badge.type}, {badge.challenge.name}", notification_type='badge_awarded')
            except Badge.DoesNotExist:
                pass