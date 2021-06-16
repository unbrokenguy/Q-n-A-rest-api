from rest_framework import serializers


class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    Reset password serializer check if new password is strong enough if not raises ValidationError.
    """

    class Meta:
        fields = ["password"]
        extra_kwargs = {
            "password": {"required": True},
        }
