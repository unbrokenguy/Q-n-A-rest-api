from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.models import HashTag


class HashTagCreateSerializer(serializers.ModelSerializer):
    """
    HashTag create data serializer.
    If HashTag with given name already exist raises ValueError.

    """

    class Meta:
        model = HashTag
        fields = ("name", "description")
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": True},
        }

    def validate(self, data):
        """
        Validates data from serializer
        Args:
            data: Serializer data - dict with hash_tag.name and question.
        Raises:
            ValidationError if hash_tag with given name already exist
        """
        if HashTag.objects.filter(name=data["name"]).first():
            raise serializers.ValidationError({"hash_tag": data["name"] + " " + _("HashTag already exist.")})

        return data
