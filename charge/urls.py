

from django.contrib import admin
from django.urls import path,include
from charge.apis.credit_request_view import CreditRequestAPIView
from charge.apis.phone_recharge_view import PhoneRechargeAPIView


urlpatterns = [
    path("credit-request/",CreditRequestAPIView.as_view(),name="credit_request"),
    path("phone-recharge/",PhoneRechargeAPIView.as_view(),name="phone_recharge"),
]

