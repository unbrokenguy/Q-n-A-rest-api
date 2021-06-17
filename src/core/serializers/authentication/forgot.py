from rest_framework import serializers

from core.serializers.validators import UserDoesNotExistValidator


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Forgot password serializer check if user with given email does not exist raises ValidationError.
    """

    email = serializers.EmailField(required=True, validators=[UserDoesNotExistValidator()])

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        raise NotImplementedError()
