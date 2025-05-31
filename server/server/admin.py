from django.contrib import admin
from .models import User, Challenge, ChallengeProgress, Badge, Post, Comment, Like, Notification, UserBadge

admin.site.register(User)
admin.site.register(Challenge)
admin.site.register(ChallengeProgress)
admin.site.register(Badge)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Notification)
admin.site.register(UserBadge)