
import factory
from django.contrib.auth.models import User
from apps.charge.models.seller_profile_model import SellerProfile
from apps.charge.models.phone_number_model import PhoneNumber



class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')


class SellerProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SellerProfile

    user = factory.SubFactory(UserFactory)
    inventory = factory.Faker('random_int', min=100, max=1000)


class PhoneNumberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PhoneNumber

    phone_number = factory.Sequence(lambda n: f'9890351134{n:03d}')  
    inventory = 0

