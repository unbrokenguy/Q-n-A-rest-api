from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User model serializer.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
        )

        extra_kwargs = {
            "email": {
                "read_only": True,
            }
        }
