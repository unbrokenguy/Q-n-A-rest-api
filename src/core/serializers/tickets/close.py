from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.models import Ticket


class TicketCloseSerializer(serializers.Serializer):
    """
    Ticket model serializer.
    Represent only id field.
    """

    id = serializers.IntegerField(required=True)

    def validate_id(self, value):
        """
        Checks if Ticket with given id exists.
        Args:
            value: Ticket id.
        Returns:
            Ticket id.
        Raises:
            ValidationError if Ticket does not exist.
        """
        try:
            Ticket.objects.get(id=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(_("Ticket does not exist."))
        return value

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        raise NotImplementedError()
