from django.db import models
from django.contrib.auth.models import User
from apps.charge.models.seller_profile_model import SellerProfile
from django.core.validators import MinValueValidator

class CreditRequest(models.Model):
    
    ACCEPTED = "accepted"
    PENDING = "pending"
    REJECTED = "rejected"

    STATUS_CHOICE = (
        (ACCEPTED, "accepted"),
        (REJECTED, "rejected"),
        (PENDING, "pending")
    )
    
    seller_profile = models.ForeignKey(SellerProfile,on_delete=models.PROTECT,related_name="credit_request")
    charge_amount = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=16,choices=STATUS_CHOICE,default=PENDING)
    previously_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "CreditRequests"
        verbose_name = "CreditRequest"
        verbose_name_plural = "CreditRequests"
    
    def __str__(self) -> str:
        return str(self.seller_profile) + str(self.charge_amount) + str(self.status)