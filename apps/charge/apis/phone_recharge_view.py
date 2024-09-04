from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers
import time
from django.db import transaction
from apps.charge.models.credit_request_model import CreditRequest
from apps.charge.models.phone_number_model import PhoneNumber
from apps.charge.models.seller_profile_model import SellerProfile
from apps.charge.models.transactions_model import Transaction
from apps.charge.serializers.phone_rechrge_serializer import PhoneRechargeSerializer
from apps.charge.tasks import process_recharge_task
from apps.charge.utils.http_exception import CustomValidationException
import logging
import json
from celery.result import AsyncResult
from logging import getLogger
logger = getLogger(__name__)

class PhoneRechargeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhoneRechargeSerializer

    def post(self, request):
        serialized_data = self.serializer_class(
            data=request.data, context={"request": request})
        serialized_data.is_valid(raise_exception=True)
        transaction_object = serialized_data.save()
        task = process_recharge_task.delay(transaction_object.id)
        return Response({"message":"عملیات در حال پردازش است",
                         "task": task.id}, status=status.HTTP_202_ACCEPTED)


class PhoneRechargeStatusAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request,task_id):
        task_result = AsyncResult(str(task_id))

        if task_result.state == 'PENDING':
            return Response({"message": "عملیات در حال انجام است."}, status=status.HTTP_202_ACCEPTED)
        elif task_result.state == 'SUCCESS':
            return Response({"message": "عملیات موفق"}, status=status.HTTP_200_OK)
        elif task_result.state == 'FAILURE':
            return Response({"message": "عملیات ناموفق"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "وضعیت نامشخص"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    