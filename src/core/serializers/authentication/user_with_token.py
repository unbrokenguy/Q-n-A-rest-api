from rest_framework import serializers
from core.serializers.authentication.user import UserSerializer
from rest_framework.authtoken.models import Token


class UserWithTokenSerializer(serializers.ModelSerializer):
    """
    User model serializer with extra authentication token field.
    """

    token = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("token",)

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key
