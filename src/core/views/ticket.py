from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.models import HashTag, Ticket
from core.serializers import (
    TicketCloseSerializer,
    TicketCreateSerializer,
    TicketSerializer,
)


class TicketViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """"""

    queryset = Ticket.objects

    serializer_class = TicketSerializer

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                "Ticket model. If user is staff returns ticket, if not only if ticket created by user.",
                TicketSerializer,
            ),
            "401": "If user is not authenticated.",
            "403": "If user is not ticket creator.",
            "404": "If ticket does not exist.",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Method to get Ticket by id, User can retrieve only his Ticket
        If User.is_staff equals True User can get any Ticket that exist.
        Returns:
            TickerSerializer with model data.
        Raises:
            HTTP_401 - If user is not authenticated,
            HTTP_403 - If user is not ticket creator,
            HTTP_404 - If ticket does not exist.
        """
        ticket = get_object_or_404(Ticket, id=kwargs["pk"])

        if not request.user.is_staff and ticket.creator is not request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            "200": openapi.Response(
                "List of Tickets. If user is staff returns all tickets, if not only tickets created by user.",
                TicketSerializer(many=True),
            ),
            "401": "If user is not authenticated.",
        },
    )
    def list(self, request, *args, **kwargs):
        """
        Method to get list of Tickets.
        User can get only Tickets that he created, but if User is staff can get all created Tickets.
        If request has parameter "?filter=HashTag.name" return only Tickets with given HashTag
        Returns:
            List of Tickets.
        Raises:
            HTTP_401 - If user is not authenticated.
        """
        query_set = Ticket.objects.all()
        hash_tag = HashTag.objects.filter(name=kwargs.get("filter")).first()

        #  If hash_tag in request parameters, filters Tickets by HashTag
        if hash_tag:
            query_set = Ticket.objects.filter(hash_tag=hash_tag)

        #  If user is not staff excludes Tickets that not created by user.
        if not request.user.is_staff:
            query_set = query_set.filter(creator=request.user)

        serializer = self.serializer_class(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=TicketCreateSerializer,
        responses={
            "201": openapi.Response("Ticket model.", TicketSerializer),
            "400": "HashTag does not exist.",
            "401": "If user is not authenticated.",
        },
    )
    def create(self, request, *args, **kwargs):
        """
        Method to create new Ticket.
        Request data - {"hash_tag": String with HashTag.name,
                        "question": String with question.
        Returns:
            TicketSerializer data with created Ticket.
        Raises:
            HTTP_400 - HashTag does not exist,
            HTTP_401 - If user is not authenticated.
        """
        serializer = TicketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = Ticket.objects.create(
            creator=request.user,
            hash_tag=HashTag.objects.get(name=serializer.validated_data["hash_tag"]["name"]),
            question=serializer.validated_data["question"],
        )

        return Response(data=self.serializer_class(ticket).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=TicketCloseSerializer,
        responses={
            "200": "",
            "400": "If Ticket already marked as archived",
            "401": "If user is not authenticated.",
            "403": "If user is not ticket creator.",
            "404": "If Ticket does not exist.",
        },
    )
    @action(methods=["POST"], detail=False)
    def close(self, request, *args, **kwargs):
        """
        Method to close ticket if user or staff decided that it solved or need to be closed.
        Tickets flag is_archived would be True, and Ticket no longer can be updated.
        Returns:
            HTTP_200 - If Ticket was archived successful,
            HTTP_400 - If Ticket already marked as archived,
            HTTP_401 - If user is not authenticated,
            HTTP_403 - If user is not ticket creator,
            HTTP_404 - If Ticket does not exist.
        """
        serializer = TicketCloseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = Ticket.objects.get(id=serializer.validated_data["id"])

        if not request.user.is_staff and ticket.creator is not request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if ticket.is_archived:
            return Response(data=_("Ticket already marked as archived."), status=status.HTTP_400_BAD_REQUEST)

        ticket.is_archived = True
        ticket.save()

        return Response(status=status.HTTP_200_OK)
