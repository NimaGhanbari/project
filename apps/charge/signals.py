
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.db import transaction

from apps.charge.models.credit_request_model import CreditRequest

from logging import getLogger
logger = getLogger(__name__)


@receiver(post_save, sender=CreditRequest)
def after_credit_request_saved(sender, instance, **kwargs):
    logger.info(f"Initiate the signal to request a credit increase for CreditRequest ID: {instance.id}")

    if instance.status == CreditRequest.ACCEPTED and instance.previously_used == False:
        logger.info(f"Processing credit request ID: {instance.id}, Charge Amount: {instance.charge_amount}")
        with transaction.atomic():
            try:
                credit_request = CreditRequest.objects.select_for_update().get(id=instance.id)
                logger.info(f"Locked CreditRequest ID: {credit_request.id} for update")
                if instance.previously_used == False:
                    seller_profile = credit_request.seller_profile
                    logger.info(f"Current inventory of SellerProfile ID: {seller_profile.id} is {seller_profile.inventory}")
                    seller_profile.inventory += instance.charge_amount
                    seller_profile.save()
                    logger.info(f"Updated inventory of SellerProfile ID: {seller_profile.id} to {seller_profile.inventory}")
                    instance.previously_used = True
                    logger.info("The credit increase was executed successfully")
                
            except Exception as e:
                logger.error(f"Credit increase encountered a problem for CreditRequest ID: {instance.id}. ERROR: {e}")
                instance.status = CreditRequest.PENDING
                logger.info(f"Set status of CreditRequest ID: {instance.id} to PENDING due to error")
        instance.save()
        
    logger.info(f"End of signal processing for CreditRequest ID: {instance.id}")
    