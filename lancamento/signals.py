from django.db.models.signals import post_save
from django.dispatch import receiver
from lancamento.models import Lancamento


@receiver(post_save, sender=Lancamento)
def update_registro(sender, instance, **kwargs):
    print(instance.id)
