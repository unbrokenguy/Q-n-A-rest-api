from rest_framework import serializers


class ConfirmEmailSerializer(serializers.Serializer):

    token = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        raise NotImplementedError()
