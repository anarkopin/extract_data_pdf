import dataclasses
from typing import TYPE_CHECKING
from . import models
import datetime
import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import secrets




#Validate to class User
if TYPE_CHECKING:
    from .models import User

#in this way we transform the dictionary of user that we receive into a class
@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    password: str
    id: int = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            id=user.id,
        )


def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    instance = models.User(
        first_name=user_dc.first_name,
        last_name=user_dc.last_name,
        email=user_dc.email,
    )
    if user_dc.password is not None:
        instance.set_password(user_dc.password)
    
    instance.save()

    return UserDataClass.from_instance(instance)

def user_email_selector(email: str) -> "User":
    try: 
        user = models.User.objects.get(email=email)
    except models.User.DoesNotExist:
        return None
    
    return user

def create_token(user_id: int) -> str:
    payload = dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        iat = datetime.datetime.utcnow()
    )

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token


def send_action_email(user_id: int, action: str) -> None:
    user = User.objects.get(id=user_id)

    if action == 'verify':
        # Generate verification code and save it to user model
        verification_code = generate_verification_code()
        user.verification_code = verification_code
        user.save()

        # Send email to user
        subject = 'Verify your account'
        message = render_to_string('verify_email.html', {'verification_code': verification_code})
        plain_message = strip_tags(message)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, plain_message, from_email, recipient_list, html_message=message)


def generate_verification_code(length=6):
    """
    Generates a random verification code with the specified length (default is 6).
    The code is a string of random digits.
    """
    return "".join(secrets.choice("0123456789") for _ in range(length))