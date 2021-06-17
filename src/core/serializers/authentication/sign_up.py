from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    """
    Sign up data serializer.
    If user already exist raises Validation Error.
    Also check password if it strong enough.
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")
        extra_kwargs = {
            "email": {"required": True, "validators": []},
            "password": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, data):
        """
        Validates data from serializer
        Args:
            data: Serializer data - dict with email, first_name, last_name and password
        Raises:
            ValidationError if user with email already exist or password is not strong enough.
        """
        if User.objects.filter(email=data["email"]).first():
            raise serializers.ValidationError({"email": _("User with this email already exist.")})

        user = User(
            username=data["email"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        password = data["password"]
        try:
            validate_password(password, user)
        except ValidationError as error:
            raise serializers.ValidationError({"password": eval(str(error))})  # Maybe Insecure
        return data
