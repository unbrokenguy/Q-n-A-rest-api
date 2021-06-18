from django.db import models


class HashTag(models.Model):
    """
    HashTag Django ORM model
    HashTag is needed to divide tickets into categories
    To make it easier to sort similar questions
    Attributes:
        name: String - Name of HashTag category.
        description: String - Description of HashTag.
    """

    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=255, blank=True)
