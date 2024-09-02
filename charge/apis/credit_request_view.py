from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import serializers


from charge.models.credit_request_model import CreditRequest
from charge.utils.http_exception import CustomValidationException


class CreditRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    class InputDataSerializer(serializers.ModelSerializer):
        class Meta:
            model = CreditRequest
            fields = [
                "charge_amount",
            ]

        def validate(self, data):
            
            seller_profile = data['seller_profile'] = self.context['request'].user.seller_profile
            if not seller_profile:
                raise CustomValidationException(
                    detail={'message': "پروفایل یافت نشد"}, status_code=status.HTTP_404_NOT_FOUND)
            
            credit_request_object = CreditRequest.objects.filter(seller_profile=seller_profile,
                                         status__in=[CreditRequest.ACCEPTED, CreditRequest.PENDING]
                                         ).first()
            
            print("credit_request_object: ", credit_request_object)
            if credit_request_object:
                raise CustomValidationException(
                    detail={'message': "شما قبلا درخواست ثبت کردید"}, status_code=status.HTTP_400_BAD_REQUEST)

            # TODO: Check
            return data

    def post(self, request):

        serialized_data = self.InputDataSerializer(
            data=request.data, context={"request": request})
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()

        return Response({"message": "درخواست افزایش اعتبار با موفقیت ثبت شد"}, status=status.HTTP_200_OK)
