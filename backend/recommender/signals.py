from recommender.models import Similarity

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType


@receiver(post_save, sender=Similarity)
def create_reverse(sender, instance, created, **kwargs):
    try:
        getattr(instance, "skip_signal")
    except:
        instance.skip_signal = False
    if created:
        if instance.skip_signal:
            return
        obj = sender(
            content_type=ContentType.objects.get_for_model(instance.source),
            source_id=instance.target_id,
            target_id=instance.source_id,
            score=instance.score,
        )
        obj.skip_signal = True
        obj.save()
        obj.skip_signal = False
    else:
        sender.objects.filter(
            content_type=ContentType.objects.get_for_model(instance.source),
            source_id=instance.target_id,
            target_id=instance.source_id,
        ).update(score=instance.score)


@receiver(post_delete, sender=Similarity)
def delete_reverse(sender, instance, using, **kwargs):
    try:
        obj = sender.objects.get(
            content_type=ContentType.objects.get_for_model(instance.source),
            source_id=instance.target_id,
            target_id=instance.source_id,
        )
        obj.delete()
    except:
        return
