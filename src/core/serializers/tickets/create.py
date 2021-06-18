from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.models import HashTag, Ticket


class TicketCreateSerializer(serializers.ModelSerializer):
    """
    Ticket create data serializer.
    If HashTag with given name does not exist raises ValueError.
    """

    hash_tag = serializers.CharField(source="hash_tag.name")

    class Meta:
        model = Ticket
        fields = ("hash_tag", "question")
        extra_kwargs = {
            "hash_tag": {"required": True},
            "question": {"required": True},
        }

    def validate(self, data):
        """
        Validates data from serializer
        Args:
            data: Serializer data - dict with hash_tag.name and question.
        Raises:
            ValidationError if hash_tag with given name does not exist
        """
        if HashTag.objects.filter(name=data["hash_tag"]["name"]).first() is None:
            raise serializers.ValidationError(
                {"hash_tag": data["hash_tag"]["name"] + " " + _("HashTag does not exist.")}
            )

        return data
