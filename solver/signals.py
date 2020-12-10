from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BoxValue, Parent


@receiver(post_save, sender=Parent)
def create_boxes(sender, instance, created, **kwargs):
    if created:
        for i in range(0, 81):
            BoxValue.objects.create(parent=instance, box_index=i)

