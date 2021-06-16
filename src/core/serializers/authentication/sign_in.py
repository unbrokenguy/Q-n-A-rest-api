from rest_framework import serializers

from core.models import User
from core.serializers.validators import UserDoesNotExistValidator


class UserSignInSerializer(serializers.ModelSerializer):
    """
    Sign in data serializer.
    If user does not exist raises Validation Error.
    """

    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {
            "email": {"required": True, "validators": [UserDoesNotExistValidator()]},
            "password": {"required": True},
        }
