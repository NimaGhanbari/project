from django.test import TestCase,TransactionTestCase
from apps.charge.models.seller_profile_model import SellerProfile
from apps.charge.models.phone_number_model import PhoneNumber
from apps.charge.models.transactions_model import Transaction
from apps.charge.tasks import process_recharge_task
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import transaction
from django.contrib.auth.models import User
from apps.charge.utils.calculate_expected_inventory import calculate_expected_inventory
import time
from apps.charge.tests.factories import UserFactory, SellerProfileFactory, PhoneNumberFactory


class PhoneRechargeTestCase(TransactionTestCase):
    def setUp(self):
        self.transaction_count = 1000
        self.charge_amount = 5

        required_inventory = self.transaction_count * self.charge_amount

        self.user1 = UserFactory(username='nima_fake')
        self.user2 = UserFactory(username='ahmad')

        self.seller1 = SellerProfileFactory(
            user=self.user1, inventory=required_inventory)
        self.seller2 = SellerProfileFactory(
            user=self.user2, inventory=required_inventory)

        self.phone1 = PhoneNumberFactory(phone_number="989035113419")
        self.phone2 = PhoneNumberFactory(phone_number="989119693978")

    def process_transactions(self, seller, phone, charge_amount, count):
        for i in range(count):
            print(f"Processing transaction {i+1}/{count} for seller {seller.id}")
            with transaction.atomic():
                transaction_object = Transaction.objects.create(
                    seller_profile=seller,
                    phone_number=phone,
                    charge_amount=charge_amount
                )
                print(f"Transaction Created: {transaction_object.id}")
                result = process_recharge_task.delay(transaction_object.id)

    def test_bulk_transactions(self):
        print("start test_bulk_transaction ----")
        
        self.process_transactions(self.seller1,self.phone1, self.charge_amount, self.transaction_count)
        self.process_transactions(self.seller2,self.phone2, self.charge_amount, self.transaction_count)
        

        self.seller1.refresh_from_db()
        self.seller2.refresh_from_db()
        self.phone1.refresh_from_db()
        self.phone2.refresh_from_db()

        expected_inventory_seller1 = self.seller1.inventory - \
            (self.transaction_count * self.charge_amount)
        expected_inventory_seller2 = self.seller2.inventory - \
            (self.transaction_count * self.charge_amount)
        expected_inventory_phone1 = self.transaction_count * self.charge_amount
        expected_inventory_phone2 = self.transaction_count * self.charge_amount

        
        self.assertEqual(self.seller1.inventory, expected_inventory_seller1,
                         f"موجودی فروشنده 1 اشتباه است. موجودی فعلی: {self.seller1.inventory}")
        self.assertEqual(self.seller2.inventory, expected_inventory_seller2,
                         f"موجودی فروشنده 2 اشتباه است. موجودی فعلی: {self.seller2.inventory}")
        self.assertEqual(self.phone1.inventory, expected_inventory_phone1,
                         f"موجودی شماره تلفن 1 اشتباه است. موجودی فعلی: {self.phone1.inventory}")
        self.assertEqual(self.phone2.inventory, expected_inventory_phone2,
                         f"موجودی شماره تلفن 2 اشتباه است. موجودی فعلی: {self.phone2.inventory}")
        succeeded_transactions = Transaction.objects.filter(
            status=Transaction.SUCCEEDED).count()
        self.assertEqual(succeeded_transactions, self.transaction_count * 2,
                         f"تعداد تراکنش‌های موفقیت‌آمیز: {succeeded_transactions}")
