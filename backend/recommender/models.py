from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Similarity(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="similarities"
    )
    source_id = models.PositiveIntegerField()
    source = GenericForeignKey("content_type", "source_id")

    target_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "target_id")

    score = models.DecimalField(max_digits=4, decimal_places=3)

    def __str__(self) -> str:
        return f"{self.content_type.model}: {self.source_id} and {self.target_id} score {self.score:.3f}"
