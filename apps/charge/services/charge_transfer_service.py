from rest_framework import status

from apps.charge.utils.http_exception import CustomValidationException

from logging import getLogger
logger = getLogger(__name__)

def transfer_service(charge_amount,seller_profile,phone_number):
    logger.info(f"Initiating transfer of {charge_amount} units from seller {seller_profile} to phone number {phone_number}")
    
    if seller_profile.inventory < charge_amount:
        logger.error(f"Insufficient inventory for seller {seller_profile}: requested {charge_amount}, available: {seller_profile.inventory}")
        raise CustomValidationException(
            detail={'message': "عدم موجودی"}, status_code=status.HTTP_400_BAD_REQUEST)
    seller_profile.inventory -= charge_amount
    seller_profile.save()
    logger.info(f"Deducted {charge_amount} units from seller {seller_profile}. New inventory: {seller_profile.inventory}")
    phone_number.inventory += charge_amount
    phone_number.save()
    logger.info(f"Added {charge_amount} units to phone number {phone_number}. New inventory: {phone_number.inventory}")

    logger.info(f"Transfer completed successfully from seller {seller_profile} to phone number {phone_number}")

        