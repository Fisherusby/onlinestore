import uuid

from django.db import models


class BaseModel(models.Model):
    # flake8: noqa: A003
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(
        null=False,
        auto_now_add=True,
        editable=False,
    )
    edited_at = models.DateTimeField(
        null=True,
        auto_now=True,
        editable=False,
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
