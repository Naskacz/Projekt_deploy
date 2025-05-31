from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password,make_password
from ..models import User

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta: 
        model = User
        fields = ['username','email','password']
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Użytkownik o takim emailu już istnieje.")
        return value
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Użytkownik o takim pseudonimie już istnieje.")
        return value
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Nieprawidłowy email lub hasło.")
        if not check_password(password, user.password):
            raise serializers.ValidationError("Nieprawidłowy email lub hasło.")
        self.user = user
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Nie znaleziono użytkownika o takim emailu.")
        return value

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        user = User.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()
        return user