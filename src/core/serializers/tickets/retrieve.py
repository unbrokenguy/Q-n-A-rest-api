from rest_framework import serializers

from core.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """
    Ticket model serializer.
    Represent all fields, but returns hash_tag as its name not id.
    """

    hash_tag = serializers.CharField(source="hash_tag.name")

    class Meta:
        model = Ticket
        fields = "__all__"
