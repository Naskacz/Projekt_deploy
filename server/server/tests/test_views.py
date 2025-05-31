from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from server.models import User, Post, Badge, UserBadge
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import override_settings

@override_settings(ROOT_URLCONF='server.urls')

class SignUpViewTest(APITestCase):
    def test_signup_success(self):
        url = reverse('sign_up')
        data = {"username": "newuser", "email": "newuser@example.com", "password": "newpass123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_signup_duplicate_email(self):
        User.objects.create_user(username="exists", email="exists@example.com", password="pass123")
        url = reverse('sign_up')
        data = {"username": "otheruser", "email": "exists@example.com", "password": "newpass"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="loginuser", email="login@example.com", password="mypassword")

    def test_login_success(self):
        url = reverse('token_obtain_pair')
        data = {"email": "login@example.com", "password": "mypassword"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_fail(self):
        url = reverse('token_obtain_pair')
        data = {"email": "login@example.com", "password": "wrongpassword"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="resetuser", email="reset@example.com", password="oldpass")

    def test_password_reset_success(self):
        url = reverse('reset_password')
        data = {"email": "reset@example.com", "new_password": "newpass123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass123"))

    def test_password_reset_invalid_email(self):
        url = reverse('reset_password')
        data = {"email": "noone@example.com", "new_password": "pass123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class FollowUserViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="follower", email="follower@example.com", password="pass")
        self.target_user = User.objects.create_user(username="followed", email="followed@example.com", password="pass")
        self.client.force_authenticate(user=self.user)

    def test_follow_user_success(self):
        url = reverse('follow_user') 
        data = {"username": self.target_user.username}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_follow_user_invalid_username(self):
        url = reverse('follow_user')
        data = {"username": 9999}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

class UserBadgesViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@example.com", password="pass123")
        self.badge = Badge.objects.create(name="Test Badge", description="desc", type="complete_challenge")
        self.user_badge = UserBadge.objects.create(user=self.user, badge=self.badge)
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_get_user_badges_success(self):
        url = reverse('user_badges', kwargs={'username': self.user.username})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['badge']['id'], self.badge.id)  # lub inna struktura zależnie od serializera

    def test_get_user_badges_user_not_found(self):
        url = reverse('user_badges', kwargs={'username': 9999})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ListUserPostsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="poster", email="poster@example.com", password="pass")
        self.other_user = User.objects.create_user(username="other", email="other@example.com", password="pass")
        Post.objects.create(creator=self.user, name="Post 1")
        Post.objects.create(creator=self.user, name="Post 2")
        Post.objects.create(creator=self.other_user, name="Other user's post")
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_list_user_posts(self):
        url = reverse('list_user_posts', kwargs={'username': self.user.username})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(post['creator'] == self.user.id for post in response.data))

    def test_list_user_posts_no_auth(self):
        url = reverse('list_user_posts', kwargs={'username': self.user.username})
        response = self.client.get(url)
        # zależy od tego czy endpoint ma permission_classes, jeśli nie ma to 200, jeśli ma - 401
        # Jeśli ma IsAuthenticated, test powinien spodziewać się 401:
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class GetUserProfileDataTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="profileuser", email="profile@example.com", password="pass")

    def test_get_userprofile_data_success(self):
        url = reverse('get_userprofile_data', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_get_userprofile_data_user_not_found(self):
        url = reverse('get_userprofile_data', kwargs={'username': 'no_such_user'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)