from django.db import models
from django.core.validators import MinValueValidator

class PhoneNumber(models.Model):
    name = models.CharField(max_length=64,blank=True,null=True)
    phone_number = models.CharField(max_length=16,unique=True)
    inventory = models.PositiveBigIntegerField(default=0,validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "PhoneNumbers"
        verbose_name = "PhoneNumber"
        verbose_name_plural = "PhoneNumbers"
        
    def __str__(self) -> str:
        return str(self.phone_number) +"-"+ str(self.inventory)