from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone

def get_local_date():
    return timezone.localtime().date()

class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    last_login = None

    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    join_date = models.DateField(default=get_local_date, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name="followers", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Challenge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=100)
    frequency = models.IntegerField(default=1)
    duration = models.IntegerField(default=30)
    is_public = models.BooleanField(default=False)
    create_date = models.DateField(default=get_local_date)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True, related_name='created_challenges')
    def __str__(self):
        return self.name
    
class ChallengeProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    start_date = models.DateField(default=get_local_date)
    last_updated = models.DateField(default=get_local_date)
    is_active = models.BooleanField(default=True)
    streak = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'challenge')
    def __str__(self):
        return str(self.progress)
    
    @property
    def percent_complete(self):
        if self.challenge.duration == 0:
            return 0
        return (self.progress / self.challenge.duration) * 100
    
BADGE_TYPES = [
    ('halfway_there', '50% Complete'),
    ('complete_challenge', '100% Complete'),
    ('streak_7_days', '7-Day Streak'),
    ('streak_30_days', '30-Day Streak'),
]


class Badge(models.Model):
    type = models.CharField(max_length=50, choices=BADGE_TYPES)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    def __str__(self):
        return self.type
    
class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    user_badge = models.ForeignKey(UserBadge, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    description = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'post')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    notification_type = models.CharField(max_length=50)
