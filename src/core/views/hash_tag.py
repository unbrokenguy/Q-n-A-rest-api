from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.models import HashTag
from core.serializers import HashTagCreateSerializer, HashTagSerializer


class HashTagViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = HashTagSerializer
    queryset = HashTag.objects

    @swagger_auto_schema(
        request_body=HashTagCreateSerializer,
        responses={
            "200": openapi.Response(
                "HashTag model.",
                HashTagSerializer,
            ),
            "400": "If HashTag already exist.",
            "401": "If user is not authenticated.",
            "403": "If user is not staff.",
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Creates new HashTag with name and description from request
        Returns:
            200 - Created HashTag model.
            400 - If HashTag with given name already exist.
            401 - If user is not authenticated,
            403 - If user is not staff.
        """
        serializer = HashTagCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = self.serializer_class(serializer.create(serializer.validated_data))
        return Response(data=data.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                "List of HashTag models.",
                HashTagSerializer(many=True),
            ),
            "401": "If user is not authenticated.",
            "403": "If user is not staff.",
        }
    )
    def list(self, request, *args, **kwargs):
        """
        Get all HashTag objects and return list.
        Returns:
            # 200 - List of all HashTag models,
            401 - If user is not authenticated,
            403 - If user is not staff,
        }
        """
        query_set = HashTag.objects.all()

        data = self.serializer_class(query_set, many=True)
        return Response(data=data.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                "HashTag model.",
                HashTagSerializer,
            ),
            "401": "If user is not authenticated.",
            "403": "If user is not staff.",
            "404": "If HashTag does not exist.",
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Tries to get HashTag model by id from request and then return it
        If object does not exist returns 404.
        Returns:
            200 - Serialized HashTag model.
            401 - If user is not authenticated,
            403 - If user is not staff,
            404 - If HashTag does not exist."
        """
        try:
            query_set = HashTag.objects.get(id=kwargs["pk"])

            data = self.serializer_class(query_set)
            return Response(data=data.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(_("HashTag does not exist."), status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={
            "200": "If HashTag deleted successfully",
            "401": "If user is not authenticated.",
            "403": "If user is not staff.",
            "404": "If HashTag does not exist.",
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Tries to get HashTag model by id from request and then delete it, if object does not exist returns 404.
        Returns:
            200 - If HashTag deleted successfully,
            401 - If user is not authenticated,
            403 - If user is not staff,
            404 - If HashTag does not exist.
        """
        try:
            hash_tag = HashTag.objects.get(id=kwargs["pk"])
            hash_tag.delete()

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(_("HashTag does not exist."), status=status.HTTP_404_NOT_FOUND)
