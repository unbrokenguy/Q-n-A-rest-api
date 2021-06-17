import datetime
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TokenTypeEnum(models.TextChoices):
    """
    Enum with token types.
    User need EMAIL VERIFICATION token to verify email.
    User need RESET PASSWORD to reset password.
    """

    EMAIL_VERIFICATION = _("EMAIL VERIFICATION")
    RESET_PASSWORD = _("RESET PASSWORD")


class Token(models.Model):
    """
    Token Django ORM model - token user can verify email and reset password.
    Attributes:
        value: String - uuid4 string.
        token_type: String - One of TokenTypeEnum value.
        expiration_date: DateTime - time when token will be expire.
        user: Foreign key to User model.
    """

    value = models.CharField(max_length=200)
    token_type = models.CharField(
        max_length=55, choices=TokenTypeEnum.choices, default=TokenTypeEnum.EMAIL_VERIFICATION
    )
    expiration_date = models.DateTimeField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Override Model.save() method we can set value to uuid4 and
        expiration_time to now() + VERIFICATION_TOKEN_EXPIRATION_TIME from settings
        Args:
            *args: Model Parameters.
            **kwargs: Model Parameters.
        """
        self.value = uuid.uuid4()
        self.expiration_date = timezone.now() + datetime.timedelta(seconds=settings.VERIFICATION_TOKEN_EXPIRATION_TIME)
        super(Token, self).save(*args, **kwargs)
