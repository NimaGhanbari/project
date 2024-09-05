from apps.charge.models.credit_request_model import CreditRequest
from apps.charge.models.transactions_model import Transaction

from logging import getLogger
logger = getLogger(__name__)


def calculate_expected_inventory(seller_profile_id):
    logger.info(f"Calculating expected inventory for seller profile ID: {seller_profile_id}")
    bounch_transactions = Transaction.objects.filter(
        seller_profile_id=seller_profile_id, status=Transaction.SUCCEEDED)
    logger.info(f"Fetched {bounch_transactions.count()} successful transactions for seller profile ID: {seller_profile_id}")
    bounch_credit_requests_accepted = CreditRequest.objects.filter(
        seller_profile__id=seller_profile_id, status=CreditRequest.ACCEPTED)
    logger.info(f"Fetched {bounch_credit_requests_accepted.count()} accepted credit requests for seller profile ID: {seller_profile_id}")
    
    amount_charged = 0
    amount_charge_used = 0
    amount_charged = sum(
        credit_request.charge_amount for credit_request in bounch_credit_requests_accepted)
    logger.info(f"Total charged amount for seller profile ID {seller_profile_id}: {amount_charged}")
    amount_charge_used = sum(
        transaction.charge_amount for transaction in bounch_transactions)
    logger.info(f"Total used amount for seller profile ID {seller_profile_id}: {amount_charge_used}")
    expected_inventory = amount_charged - amount_charge_used
    logger.info(f"Expected inventory for seller profile ID {seller_profile_id}: {expected_inventory}")
    return expected_inventory
