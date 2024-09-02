from charge.models.phone_number_model import PhoneNumber
from django_project.celery import app
from charge.models.transactions_model import Transaction
from charge.models.seller_profile_model import SellerProfile
from django.db import transaction
import logging
from charge.utils.http_exception import CustomValidationException
from rest_framework import status
from celery import shared_task

@app.task()
def process_recharge_task(transaction_id):
    
    try:
        with transaction.atomic():
            transaction_object = Transaction.objects.select_for_update().get(id=transaction_id)
            seller_profile = SellerProfile.objects.select_for_update().get(
                id=transaction_object.seller_profile.id)
            phone_number = PhoneNumber.objects.select_for_update().get(
                id=transaction_object.phone_number.id)

            if seller_profile.inventory < transaction_object.charge_amount:
                out_of_stock = True
                raise Exception
            
            seller_profile.inventory -= transaction_object.charge_amount
            seller_profile.save()
            phone_number.inventory += transaction_object.charge_amount
            phone_number.save()
            transaction_object.status = Transaction.SUCCEEDED
            transaction_object.save()
    except Exception as e:
        logging.error(f"ERROR: {e}")
        transaction_object.status = Transaction.FAILED
        transaction_object.save()
        if out_of_stock:
            raise CustomValidationException(
                detail={'message': "عدم موجودی"}, status_code=status.HTTP_400_BAD_REQUEST)
        raise CustomValidationException(
            detail={'message': "عملیات ناموفق"}, status_code=status.HTTP_400_BAD_REQUEST)