from django.db import models


class Ticket(models.Model):
    """
    Ticket Django ORM model
    Questions asked by users, they can choose the HashTag of the question
    Attributes:
        creator: ForeignKey to User creator of ticket.
        hash_tag: ForeignKey to HashTag, type of ticket.
        question: String with question, max length is 4000 because of telegram restrictions.
        is_archived: Boolean, True if ticket marked as solved or closed.
    """

    creator = models.ForeignKey("User", on_delete=models.CASCADE)
    hash_tag = models.ForeignKey("HashTag", on_delete=models.CASCADE, blank=False)
    question = models.CharField(max_length=4000, blank=False)
    is_archived = models.BooleanField(default=False)
