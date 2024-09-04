from apps.charge.models.phone_number_model import PhoneNumber
from apps.charge.utils.calculate_expected_inventory import calculate_expected_inventory
from charge_hub_project.celery import app
from apps.charge.models.transactions_model import Transaction
from apps.charge.models.seller_profile_model import SellerProfile
from django.db import transaction
import logging
from apps.charge.utils.http_exception import CustomValidationException
from rest_framework import status
from celery import shared_task
import time


@app.task()
def process_recharge_task(transaction_id):

    try:
        with transaction.atomic():
            transaction_object = Transaction.objects.select_for_update().get(id=transaction_id)
            seller_profile = SellerProfile.objects.select_for_update().get(
                id=transaction_object.seller_profile.id)
            phone_number = PhoneNumber.objects.get(id=transaction_object.phone_number.id)
            seller_profile.reduce_inventory(transaction_object.charge_amount)
            phone_number.increase_inventory(transaction_object.charge_amount)
            
            transaction_object.status = Transaction.SUCCEEDED
            transaction_object.save()
            assert seller_profile.inventory == calculate_expected_inventory(seller_profile.id), "Inventory check failed!"
    except Exception as e:
        logging.error(f"ERROR: {e}")
        transaction_object.status = Transaction.FAILED
        transaction_object.save()
        raise e