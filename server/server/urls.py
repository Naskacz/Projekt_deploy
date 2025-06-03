"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from .views.user_views import (
    get_user,
    sign_up,
    reset_password,
    follow_user,
    unfollow_user,
    CustomTokenObtainPairView,
    get_followers,
    get_following,
    get_userprofile_data
)
from .views.challenge_views import (
    create_challenge,
    list_challenges,
    list_user_challenges,
    list_user_praticipate_challenges
)
from .views.userbadge_views import get_user_badges

from .views.post_views import(
    list_user_posts,
    post_counts,
    create_post
    )
from .views.challengeprogress_views import (
    create_challenge_progress,
    increment_progress,
    activate_or_deactivate_challenge,
    get_user_challenge_progress
    )

from .views.comment_views import (
    post_comment,
    delete_comment,
    get_comments
    )

from .views.like_views import (
    post_like,
    delete_like,
    )

from .views.notification_views import NotificationViewSet

from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notifications')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/get_user/', get_user, name='get_user'),
    path('api/signup/', sign_up, name='sign_up'),
    path('api/reset_password/', reset_password, name='reset_password'),
    path('api/follow_user/', follow_user, name='follow_user'),
    path('api/unfollow_user/', unfollow_user, name='unfollow_user'),
    path('api/create_challenge/', create_challenge, name='create_challenge'),
    path('api/list_challenges/', list_challenges, name='list_challenges'),
    path('api/my-challenges/', list_user_challenges, name='my_challenges'),
    path('api/my-challenges-participate/', list_user_praticipate_challenges, name='my_challenges_participate'),

    path('api/userprofile/<str:username>/', get_userprofile_data, name='get_userprofile_data'),
    path('api/get_followers/<str:username>/', get_followers, name='get_followers'),
    path('api/get_following/<str:username>/', get_following, name='get_following'),
  
    path('api/users/<str:username>/badges/', get_user_badges, name='user_badges'),
  
    path('api/challenge-progress/create/', create_challenge_progress, name='challenge-progress-create'),
    path('api/increment_progress/', increment_progress, name='increment_progress'),

    # post
    path('api/posts/create_post/', create_post, name='create_post'),
    path('api/list_user_posts/<str:username>/', list_user_posts, name='list_user_posts'),
    path('api/<int:post_id>/comment/', post_comment, name='post_comment'),
    path('api/<int:comment_id>/uncomment/', delete_comment, name='delete_comment'),
    path('api/<int:post_id>/comments/', get_comments, name='get_comments'),
    path('api/<int:post_id>/like/', post_like, name='post_like'),
    path('api/<int:post_id>/unlike/', delete_like, name='delete_like'),
    path('api/posts/post_counts', post_counts, name='post_counts'),
  
    path('api/activate_or_deactivate_challenge/', activate_or_deactivate_challenge, name='activate_or_deactivate_challenge'),
    path('api/', include(router.urls)),
    path('api/challenge-progress/<int:challenge_id>/', get_user_challenge_progress, name='get_user_challenge_progress'),
]
