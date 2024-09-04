
from apps.charge.models.credit_request_model import CreditRequest
from apps.charge.models.transactions_model import Transaction


def calculate_expected_inventory(seller_profile_id):
    bounch_transactions = Transaction.objects.filter(
        seller_profile_id=seller_profile_id, status=Transaction.SUCCEEDED)
    bounch_credit_requests_accepted = CreditRequest.objects.filter(
        seller_profile__id=seller_profile_id, status=CreditRequest.ACCEPTED)

    amount_charged = 0
    amount_charge_used = 0
    amount_charged = sum(
        credit_request.charge_amount for credit_request in bounch_credit_requests_accepted)
    amount_charge_used = sum(
        transaction.charge_amount for transaction in bounch_transactions)
    expected_inventory = amount_charged - amount_charge_used
    return expected_inventory
