from apps.charge.utils.http_exception import CustomValidationException
from rest_framework import serializers
from apps.charge.models.transactions_model import Transaction
from apps.charge.models.phone_number_model import PhoneNumber
from rest_framework import status



class PhoneRechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "phone_number",
            "charge_amount"
        ]

    def to_internal_value(self, data):
        if "phone_number" not in data or not data["phone_number"]:
            raise CustomValidationException(
                detail={'message': "شماره تلفن مورد نظر را وارد کنید"}, status_code=status.HTTP_400_BAD_REQUEST)
        phone_number_object = PhoneNumber.objects.filter(
            phone_number=data["phone_number"]).first()
        if not phone_number_object:
            raise CustomValidationException(
                detail={'message': "شماره تلفن مورد نظر یافت نشد"}, status_code=status.HTTP_404_NOT_FOUND)
        data["phone_number"] = phone_number_object.id
        return super().to_internal_value(data)

    def validate(self, data):
        if "charge_amount" not in data or not data["charge_amount"]:
            raise CustomValidationException(
                detail={'message': "مقدار شارژ را وارد کنید"}, status_code=status.HTTP_400_BAD_REQUEST)
        if data["charge_amount"] <= 0:
            raise CustomValidationException(
                detail={'message': "مقدار شارژ اشتباه وارد شده است"}, status_code=status.HTTP_400_BAD_REQUEST)
        seller_profile = data['seller_profile'] = self.context['request'].user.seller_profile
        if not seller_profile:
            raise CustomValidationException(
                detail={'message': "پروفایل یافت نشد"}, status_code=status.HTTP_404_NOT_FOUND)

        return data
    