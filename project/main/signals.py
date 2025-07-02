from datetime import datetime

from asgiref.sync import async_to_sync

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from main.models import MassSendMessage

from .utils.signals import run_background_task_with_delay


@receiver(post_save, sender=MassSendMessage)
def check_delay_time_by_mass_message(sender, instance, created, **kwargs):
    if created:
        if instance.delay_time and instance.send_to:
            # print('here')
            async_to_sync(run_background_task_with_delay)(instance.name)