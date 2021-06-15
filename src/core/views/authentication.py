from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.utils.translation import gettext_lazy as _

from core.models import User, Token, TokenTypeEnum
from core.serializers import UserWithTokenSerializer, UserSignInSerializer, UserSignUpSerializer, \
    ConfirmEmailSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from core.services import send_email_verification, send_reset_password_email


class AuthenticationViewSet(GenericViewSet):
    """
    Authentication View Set, handle sign in and sign up process and etc.
    """

    serializer_class = UserWithTokenSerializer
    permission_classes_by_action = {"send_confirmation_email": [IsAuthenticated], "set_telegram_id": [IsAuthenticated]}

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [AllowAny()]

    @swagger_auto_schema(
        request_body=UserSignInSerializer,
        responses={
            "200": openapi.Response("User with token field", UserWithTokenSerializer),
            "400": "User with this email does not exist.",
        },
    )
    @action(methods=["POST"], detail=False)
    def sign_in(self, request, *args, **kwargs):
        """
        Authenticate User to the system and return User data with authorization token
        Or if User does not exist or no email in request data.
        Returns:
            User model with auth_token field or 400.
        Raises:
            Validation Error if User does not exist or no email in request data.
        """
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = request.data
        user = authenticate(
            request,
            email=data["email"],
            password=data["password"],
        )
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(self.serializer_class(user, context={"request": request}).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserSignUpSerializer,
        responses={
            "201": openapi.Response("User with token field", UserWithTokenSerializer),
            "400": "User with this email already exist or Validation errors - {error_type: [error_list].",
        },
    )
    @action(methods=["POST"], detail=False)
    def sign_up(self, request, *args, **kwargs):
        """
        Register User in the system returns User with authentication token field
        Or http 400 error if not all fields are present in request data, user already exist and password validation errors.
        Returns:
            User model with auth_token field or 400 if password too weak.
        Raises:
            Validation if not all fields are present in request data, user already exist and password validation errors.
        """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User(
            username=serializer.validated_data["email"],
            email=serializer.validated_data["email"],
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
        )

        user.set_password(serializer.validated_data["password"])
        user.save()

        token = Token.objects.create(user=user, token_type=TokenTypeEnum.EMAIL_VERIFICATION)
        send_email_verification(user=user, token=token)

        return Response(self.serializer_class(user, context={"request": request}).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method="POST",
        request_body=ConfirmEmailSerializer,
        responses={
            "200": openapi.Response("User with token field", UserWithTokenSerializer),
            "400": "Invalid token.",
        },
    )
    @swagger_auto_schema(
        method="GET",
        responses={
            "200": openapi.Response("User with token field", UserWithTokenSerializer),
            "400": "Invalid token.",
        },
    )
    @action(methods=["POST", "GET"], detail=False)
    def confirm_email(self, request, *args, **kwargs):
        """
        Takes request with token and if token exist verify users email else returns http 400 with Invalid token message.
        Returns:
            User model with auth_token field or 400 if token is invalid.
        Raises:
            Validation if not all fields are present in request data, user already exist and password validation errors.
        """
        # TODO token serialization in serializer

        try:
            token = Token.objects.get(
                value=request.data.get("token") or request.GET.get('token'),
                expiration_date__gt=timezone.now(),
                token_type=TokenTypeEnum.EMAIL_VERIFICATION,
            )
        except Token.DoesNotExist:
            raise ValidationError(_("Invalid Token"))

        user = token.user
        user.is_email_verified = True

        token.delete()
        user.save()
        if request.method == "GET":
            return Response(status=status.HTTP_200_OK)
        return Response(self.serializer_class(user, context={"request": request}).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    @action(methods=["POST"], detail=False)
    def forgot_password(self, request, *args, **kwargs):
        """
        Takes request and send to user email with reset token.
        Returns:
            HTTP_200_OK response
        Raises:
            ValidationError if User with given email does not exist.
        """

        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email")
        user = User.objects.get(email=email)

        request.user = user
        token = Token.objects.create(user=user, token_type=TokenTypeEnum.RESET_PASSWORD)
        send_reset_password_email(user=user, token=token)

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    @action(methods=["POST"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        """
        Takes request and if password is strong and token type is RESET_PASSWORD sets new password to user.
        Else raises ValidationError if token or password is invalid.
        Returns:
             User model with auth_token field or 400 if token or password is invalid.
        Raises:
            ValidationError if User with given email does not exist.
        """
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # TODO maybe move token and password serialization in serializer
        try:
            token = Token.objects.get(
                value=request.data.get("token"),
                expiration_date__gt=timezone.now(),
                token_type=TokenTypeEnum.RESET_PASSWORD,
            )
        except Token.DoesNotExist:
            raise ValidationError(_("Invalid token"))

        user = token.user

        request_data = request.data

        try:
            validate_password(request_data["password"], user=user)
        except ValidationError as e:
            return Response(data=[e], status=status.HTTP_400_BAD_REQUEST)

        user.set_password(request_data["password"])
        token.delete()
        user.save()

        return Response(self.serializer_class(user, context={"request": request}).data)

