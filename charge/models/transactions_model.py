from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from charge.models.phone_number_model import PhoneNumber
from charge.models.seller_profile_model import SellerProfile


class Transaction(models.Model):

    SUCCEEDED = "succeeded"
    PENDING = "pending"
    FAILED = "failed"

    STATUS_CHOICE = (
        (SUCCEEDED, "succeeded"),
        (FAILED, "failed"),
        (PENDING, "pending")
    )

    seller_profile = models.ForeignKey(
        SellerProfile, on_delete=models.PROTECT,related_name="user_transaction")
    status = models.CharField(max_length=16,choices=STATUS_CHOICE,default=PENDING)
    phone_number = models.ForeignKey(PhoneNumber,on_delete=models.SET_NULL,null=True,related_name="phone_transaction")
    charge_amount = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Transactions"
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        indexes = [
            models.Index(fields=['seller_profile']),
        ]

    def __str__(self) -> str:
        return str(self.seller_profile) + str(self.charge_amount) + str(self.status)
    