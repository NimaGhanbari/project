from django.urls import path

from apps.charge.apis.credit_request_view import CreditRequestAPIView
from apps.charge.apis.phone_recharge_view import PhoneRechargeAPIView, PhoneRechargeStatusAPIView


urlpatterns = [
    path("credit-request/",CreditRequestAPIView.as_view(),name="credit_request"),
    path("phone-recharge/",PhoneRechargeAPIView.as_view(),name="phone_recharge"),
    path("recharge-status/<uuid:task_id>",PhoneRechargeStatusAPIView.as_view(),name="recharge_status"),
]

