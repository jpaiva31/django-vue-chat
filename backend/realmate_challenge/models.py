import uuid

from django.db import models


class BaseModel(models.Model):
    """Base model para todos os modelos."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
        db_index=True
    )

    class Meta:
        abstract = True