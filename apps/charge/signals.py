
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from apps.charge.models.credit_request_model import CreditRequest
from apps.charge.models.seller_profile_model import SellerProfile
from django.db import transaction
import logging


@receiver(post_save, sender=CreditRequest)
def after_credit_request_saved(sender, instance, **kwargs):
    logging.info("Initiate the signal to request a credit increase")

    if instance.status == CreditRequest.ACCEPTED and instance.previously_used == False:
        with transaction.atomic():
            try:
                credit_request = CreditRequest.objects.select_for_update().get(id=instance.id)
                if instance.previously_used == False:
                    seller_profile = credit_request.seller_profile
                    seller_profile.inventory += instance.charge_amount
                    seller_profile.save()
                    instance.previously_used = True
                    logging.info("The credit increase was executed successfully")
                
            except Exception as e:
                logging.error(f"Credit increase was a problem. ERROR: {e}")
                instance.status = CreditRequest.PENDING
        instance.save()
        
    logging.info("End of signal to request a credit increase")