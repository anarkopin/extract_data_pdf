import pytest

from faker import Faker
from ddf import G

from tests.providers.custom_faker_providers import EmailProvider
from apps.users.models import User

#utilizando datos falsos y provider email personalizado
fake = Faker()
fake.add_provider(EmailProvider)

#No se crea registro en la base de datos

#va a poder ser pasado en los test
@pytest.fixture
def user_creation():
    return G(User)

@pytest.mark.django_db
def test_user_creation(user_creation):
    user_creation.save()
    print(user_creation.first_name)
    assert user_creation.is_active == True
    assert user_creation.is_staff == False
    assert user_creation.is_superuser == False
    assert user_creation.is_email_verified == False

@pytest.mark.django_db
def test_superuser_creation(user_creation):
    user_creation.is_staff = False
    user_creation.is_superuser = True

    assert user_creation.is_active == True
    assert user_creation.is_staff == False
    assert user_creation.is_superuser == True
    assert user_creation.is_email_verified == False

@pytest.mark.django_db
def test_staff_user_creation(user_creation):
    user_creation.is_staff = True
    user_creation.is_superuser = True

    assert user_creation.is_active == True
    assert user_creation.is_staff == True
    assert user_creation.is_superuser == True
    assert user_creation.is_email_verified == False

@pytest.mark.django_db
def test_user_creation_fail():
    with pytest.raises(Exception):
        user = User.objects.create_superuser(
            first_name="John",
            last_name="Doe",
            email="diego@gmail.com",
            password="123456",
        )











































