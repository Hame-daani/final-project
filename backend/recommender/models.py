from django.db import connection, models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Similarity(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    source_id = models.PositiveIntegerField()
    source = GenericForeignKey("content_type", "source_id")

    target_id = models.PositiveIntegerField()
    target = GenericForeignKey("content_type", "target_id")

    score = models.DecimalField(max_digits=4, decimal_places=3)

    def __str__(self) -> str:
        return f"{self.content_type.model}: {self.source_id} and {self.target_id} score {self.score:.3f}"

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE {} CASCADE".format(cls._meta.db_table))

    @classmethod
    def bulk_update_create(cls, records):
        create_records = records
        # create_records = []
        # update_records = []
        # for record in records:
        #     if cls.objects.filter(
        #         content_type=record.content_type,
        #         source_id=record.source_id,
        #         target_id=record.target_id,
        #     ).exists():
        #         pass
        # records_to_update = update_records + [
        #     Similarity(
        #         content_type=r.content_type,
        #         source_id=r.target_id,
        #         target_id=r.source_id,
        #         score=r.score,
        #     )
        #     for r in update_records
        # ]
        # cls.objects.bulk_update(records_to_update)
        records_to_create = create_records + [
            Similarity(
                content_type=r.content_type,
                source_id=r.target_id,
                target_id=r.source_id,
                score=r.score,
            )
            for r in create_records
        ]
        cls.objects.bulk_create(records_to_create)
        n = len(records_to_create)
        m = 0
        return n, m
