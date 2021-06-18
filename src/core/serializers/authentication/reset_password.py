from rest_framework import serializers

from core.models import User


class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    Reset password serializer check if new password is strong enough if not raises ValidationError.
    """

    class Meta:
        model = User
        fields = ["password"]
        extra_kwargs = {
            "password": {"required": True},
        }
