from rest_framework import status
from apps.charge.utils.http_exception import CustomValidationException


def transfer_service(charge_amount,seller_profile,phone_number):
    
    if seller_profile.inventory < charge_amount:
        raise CustomValidationException(
            detail={'message': "عدم موجودی"}, status_code=status.HTTP_400_BAD_REQUEST)
    seller_profile.inventory -= charge_amount
    seller_profile.save()
    phone_number.inventory += charge_amount
    phone_number.save()

        