from rest_framework import serializers

from core.models import HashTag


class HashTagSerializer(serializers.ModelSerializer):
    """
    HashTag model serializer.
    Represent all fields.
    """

    class Meta:
        model = HashTag
        fields = "__all__"
