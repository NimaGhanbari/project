from rest_framework import serializers
from apps.charge.models.credit_request_model import CreditRequest
from apps.charge.utils.http_exception import CustomValidationException
from rest_framework import status

class CreditRequestSerializer(serializers.ModelSerializer):
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
        
        return data