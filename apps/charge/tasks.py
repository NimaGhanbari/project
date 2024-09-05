
from django.db import transaction

from apps.charge.models.phone_number_model import PhoneNumber
from apps.charge.services.charge_transfer_service import transfer_service
from apps.charge.utils.calculate_expected_inventory import calculate_expected_inventory
from apps.charge.models.transactions_model import Transaction
from apps.charge.models.seller_profile_model import SellerProfile

from charge_hub_project.celery import app

from logging import getLogger
logger = getLogger(__name__)


@app.task()
def process_recharge_task(transaction_id):
    logger.info(f"Starting process_recharge_task for transaction ID: {transaction_id}")
    try:
        with transaction.atomic():
            logger.info("Attempting to fetch transaction object with select_for_update.")
            transaction_object = Transaction.objects.select_for_update().get(id=transaction_id)
            logger.info(f"Transaction fetched: {transaction_object}")
            
            logger.info(f"Fetching seller profile with ID: {transaction_object.seller_profile.id}")
            seller_profile = SellerProfile.objects.select_for_update().get(
                id=transaction_object.seller_profile.id)
            logger.info(f"Seller profile fetched: {seller_profile}")
            
            logger.info(f"Fetching phone number with ID: {transaction_object.phone_number.id}")
            phone_number = PhoneNumber.objects.get(
                id=transaction_object.phone_number.id)
            logger.info(f"Phone number fetched: {phone_number}")
            
            logger.info(f"Initiating transfer service for charge_amount: {transaction_object.charge_amount}")
            transfer_service(charge_amount=transaction_object.charge_amount,
                             seller_profile=seller_profile, phone_number=phone_number)
            logger.info(f"Transfer service completed successfully for transaction ID: {transaction_id}")

            transaction_object.status = Transaction.SUCCEEDED
            transaction_object.save()
            logger.info(f"Transaction status updated to SUCCEEDED for ID: {transaction_id}")

            assert seller_profile.inventory == calculate_expected_inventory(
                seller_profile.id), "Inventory check failed!"
            logger.info("Inventory check passed successfully.")
            
    except Exception as e:
        logger.error(f"ERROR during processing transaction ID: {transaction_id}. ERROR: {e}")
        transaction_object.status = Transaction.FAILED
        transaction_object.save()
        logger.info(f"Transaction status updated to FAILED for ID: {transaction_id}")
        raise e
    
    logger.info(f"process_recharge_task completed for transaction ID: {transaction_id}")
