from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from ..serializers.auth_serializers import SignUpSerializer

User = get_user_model()

def get_user_by_username(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise NotFound("Użytkownik o takiej nazwie nie istnieje")
    
def get_user_by_id(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound("Użytkownik z takim id nie istnieje")

def sign_up_service(data):
    serializer = SignUpSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()
