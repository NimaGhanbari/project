from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers
import time
from django.db import transaction
from charge.models.credit_request_model import CreditRequest
from charge.models.phone_number_model import PhoneNumber
from charge.models.seller_profile_model import SellerProfile
from charge.models.transactions_model import Transaction
from charge.tasks import process_recharge_task
from charge.utils.http_exception import CustomValidationException
import logging
import json

class PhoneRechargeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    class InputDataSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            fields = [
                "phone_number",
                "charge_amount"
            ]

        def to_internal_value(self, data):
            if "phone_number" not in data and not data["phone_number"]:
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
            print("phone: ", data["phone_number"])
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

    def post(self, request):

        serialized_data = self.InputDataSerializer(
            data=request.data, context={"request": request})
        serialized_data.is_valid(raise_exception=True)
        transaction_object = serialized_data.save()
        print("transaction_object:", transaction_object)
        result = process_recharge_task.delay(transaction_object.id)
        while True:
            if result.ready():
                break
            time.sleep(0.5)
        
        if result.state == 'SUCCESS':
            return Response({"message": "عملیات موفق"}, status=status.HTTP_200_OK)
        elif result.state == 'FAILURE':
            return Response({"message": "عملیات نا موفق"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "وضعیت نامشخص"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
