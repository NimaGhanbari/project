from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.charge.serializers.credit_request_serializer import CreditRequestSerializer

from apps.charge.models.credit_request_model import CreditRequest
from apps.charge.utils.http_exception import CustomValidationException


from logging import getLogger
logger = getLogger(__name__)

class CreditRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreditRequestSerializer
    
    def post(self, request):
        logger.info(f"Received credit request from user: {request.user}")
        
        serialized_data = self.serializer_class(
            data=request.data, context={"request": request})
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        
        logger.info(f"Credit request successfully processed for user: {request.user}")
        return Response({"message": "درخواست افزایش اعتبار با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
