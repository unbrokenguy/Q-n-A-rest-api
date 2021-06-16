from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class NoUserNameUserManager(UserManager):
    """
    Custom UserManager to override create_superuser with username = email.
    """

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        Override method from UserManager so username = email.
        Args:
            email: String with Email.
            password: String with Password.
            **extra_fields: Extra parameters to match function signature.
        """
        super().create_superuser(username=email, email=email, password=password)


class User(AbstractUser):
    """
    User Django ORM model, inherits from AbstractUser
    Attributes:
        email: EmailField - email address User sign in/up with
        is_email_verified: Boolean - True if User has verified his email address via code from email else False
        telegram_id: Integer - Users Telegram id to communicate with Bot.
    """

    email = models.EmailField(_("email address"), blank=True, unique=True)
    is_email_verified = models.BooleanField(default=False)
    telegram_id = models.PositiveBigIntegerField(null=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = NoUserNameUserManager()

    def save(self, *args, **kwargs):
        """
        Save User with given parameters from args and kwargs.
        If User not in database set user.username = user.email
        Args:
            *args: Parameters
            **kwargs: Parameters
        """
        if not self.pk:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        """
        User to string method
        Returns:
            String with User email
        """
        return self.email
