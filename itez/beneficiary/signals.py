from django.db.models.signals import pre_save
from django.dispatch import receiver

from itez.beneficiary.models import Agent, Beneficiary
from itez.beneficiary.utils import generate_uuid


@receiver(pre_save, sender=Beneficiary)
def set_beneficiary_ID(instance, sender, **kwargs):
    """
    Assigns a unique generated ID to the beneficiary object before saving to
    the database. If instance.id is None, it means the object is being updated
    hence no need to generate a new ID.
    """
    if not instance.id:
        instance.beneficiary_id = generate_uuid()[0]
    else:
        pass


@receiver(pre_save, sender=Agent)
def set_agent_ID(instance, sender, **kwargs):
    """
    Assigns a unique generated ID to the agent object before saving to
    the database. If instance.id is None, it means the object is being updated
    hence no need to generate a new ID.
    """
    if not instance.id:
        instance.agent_id = generate_uuid()[1]
    else:
        pass
