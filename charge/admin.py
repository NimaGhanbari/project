from django.contrib import admin
from charge.models.credit_request_model import CreditRequest
from charge.models.phone_number_model import PhoneNumber
from charge.models.seller_profile_model import SellerProfile
from charge.models.transactions_model import Transaction


@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    model=CreditRequest
    list_display = ["id","seller_profile","charge_amount","status","created_at"]
    search_fields = ["seller_profile__phone_number"]
    list_filter = ["status"]
    readonly_fields =["seller_profile","charge_amount"]
    list_editable = ["status"]
    
    
    
@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    model=PhoneNumber
    list_display = ["id","name","phone_number","inventory"]
    search_fields = ["phone_number"]



@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    model=SellerProfile
    list_display = ["id","user","name","inventory","is_active"]
    list_filter = ["is_active"]
    readonly_fields =["inventory"]
    

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    model=Transaction
    list_display = ["id","seller_profile","charge_amount","phone_number","status"]
    search_fields = ["phone_number__phone_number"]
    list_filter = ["status"]
    readonly_fields =["seller_profile","charge_amount"]
    