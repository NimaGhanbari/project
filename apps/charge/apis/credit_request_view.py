from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from apps.charge.serializers.credit_request_serializer import CreditRequestSerializer


from apps.charge.models.credit_request_model import CreditRequest
from apps.charge.utils.http_exception import CustomValidationException


class CreditRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreditRequestSerializer
    
    def post(self, request):

        serialized_data = self.serializer_class(
            data=request.data, context={"request": request})
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response({"message": "درخواست افزایش اعتبار با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
