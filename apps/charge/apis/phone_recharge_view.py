from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.charge.serializers.phone_rechrge_serializer import PhoneRechargeSerializer
from apps.charge.tasks import process_recharge_task

from celery.result import AsyncResult

from logging import getLogger
logger = getLogger(__name__)


class PhoneRechargeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhoneRechargeSerializer

    def post(self, request):
        logger.info(
            f"Received phone recharge request from user: {request.user}")

        serialized_data = self.serializer_class(
            data=request.data, context={"request": request})
        serialized_data.is_valid(raise_exception=True)
        transaction_object = serialized_data.save()
        logger.info(
            f"A transaction record was created by seller {transaction_object.seller_profile} in the amount of {transaction_object.charge_amount} for phone_number {transaction_object.phone_number} and is {transaction_object.status}.")
        task = process_recharge_task.delay(transaction_object.id)
        
        logger.info(f"Phone recharge processing task started with task ID: {task.id}")
        return Response({"message": "عملیات در حال پردازش است",
                         "task": task.id}, status=status.HTTP_202_ACCEPTED)


class PhoneRechargeStatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        logger.info(f"Checking status for task ID: {task_id} requested by user: {request.user}")

        task_result = AsyncResult(str(task_id))

        if task_result.state == 'PENDING':
            logger.info(f"Task {task_id} is pending.")
            return Response({"message": "عملیات در حال انجام است."}, status=status.HTTP_202_ACCEPTED)
        elif task_result.state == 'SUCCESS':
            logger.info(f"Task {task_id} completed successfully.")  
            return Response({"message": "عملیات موفق"}, status=status.HTTP_200_OK)
        elif task_result.state == 'FAILURE':
            logger.error(f"Task {task_id} failed.")
            return Response({"message": "عملیات ناموفق"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.warning(f"Task {task_id} has an unknown state: {task_result.state}.")
            return Response({"message": "وضعیت نامشخص"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
