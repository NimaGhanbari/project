from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from apps.charge.utils.http_exception import CustomValidationException
from rest_framework import status

class SellerProfile(models.Model):
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='seller_profile')
    inventory = models.PositiveBigIntegerField(default=0,validators=[MinValueValidator(0)])
    name = models.CharField(max_length=64, blank=True,null=True)
    phone_number = models.CharField(max_length=16,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "Profiles"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
    
    def __str__(self) -> str:
        return str(self.user.username)
    
    def reduce_inventory(self, amount):
        if self.inventory < amount:
            raise CustomValidationException(
                detail={'message': "عدم موجودی"}, status_code=status.HTTP_400_BAD_REQUEST)
        self.inventory -= amount
        self.save()