from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers

from core.models import User, Token, TokenTypeEnum


class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    Reset password serializer check if new password is strong enough if not raises ValidationError.
    """
    class Meta:
        fields = ["password"]
        extra_kwargs = {
            "password": {"required": True},
        }
