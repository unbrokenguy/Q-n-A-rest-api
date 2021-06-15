from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from core.models import User


class UserDoesNotExistValidator:
    def __init__(self):
        pass

    def __call__(self, value):
        """
        Validates data from serializer
        Args:
            value: String with Email
        Raises:
            ValidationError if user with email does not exist.
        """
        user = User.objects.filter(email=value).first()
        if user is None:
            raise serializers.ValidationError(_("User with this email does not exist."))
