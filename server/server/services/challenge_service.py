from ..models import Challenge

def get_common_challenges(user1, user2):
    return Challenge.objects.filter(
        challengeprogress__user=user1
    ).filter(
        challengeprogress__user=user2
    ).distinct()
