import dataclasses
from typing import TYPE_CHECKING
from .. import models
import datetime
import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import secrets
from django.db import transaction
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db import IntegrityError



#Validate to class User
if TYPE_CHECKING:
    from ..models import User, Rol


#in this way we transform the dictionary of user that we receive into a class
@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    password: str
    rol: str
    id: int = None

    def __post_init__(self):
        if not isinstance(self.rol, str):
            raise ValueError("Field 'rol' must be a string")
        
        # Verificar si el rol existe en la base de datos
        if not models.Rol.objects.filter(rol=self.rol).exists():
            raise ValueError(f"Role '{self.rol}' does not exist in the database. Please provide a valid role.")

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=None,
            rol=user.rol,
            id=user.id,
        )


def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    # Validación de entrada
    if not user_dc.first_name or not user_dc.last_name or not user_dc.email or not user_dc.rol:
        raise ValueError("First name, last name, email and rol are required fields")
    if not validate_email(user_dc.email):
        raise ValueError("Invalid email address")
    
    #obtener el rol

    try:
        rol = Rol.objects.get(rol=user_dc.rol)
    except Rol.DoesNotExist:
        raise ValueError("Role does not exist")
    
    instance = models.User(
        first_name=user_dc.first_name,
        last_name=user_dc.last_name,
        email=user_dc.email,
        rol= rol,
    )
    if user_dc.password is not None:
        instance.set_password(user_dc.password)

    try:
        instance.save()
    except IntegrityError as e:
        raise ValueError("Failed to create user: {}".format(str(e)))

    return UserDataClass.from_instance(instance)

def update_user(user_dc: "UserDataClass") -> "UserDataClass":
    try:
        # Buscar la instancia del usuario en la base de datos por su ID
        instance = models.User.objects.get(id=user_dc.id)
        
        # Actualizar los campos del usuario con los valores del objeto UserDataClass
        instance.first_name = user_dc.first_name
        instance.last_name = user_dc.last_name
        instance.email = user_dc.email
        instance.rol = user_dc.rol
        
        # Validar y actualizar la contraseña solo si se proporciona en UserDataClass
        if user_dc.password is not None:
            instance.set_password(user_dc.password)
        
        instance.save()  # Guardar los cambios en la base de datos
        
        return UserDataClass.from_instance(instance)
    
    except models.User.DoesNotExist:
        # Manejar el caso en que el usuario no existe en la base de datos
        raise ValueError("El usuario especificado no existe")

    except Exception as e:
        # Manejar otros posibles errores, como errores de base de datos u otros
        raise Exception("Error al actualizar el usuario: {}".format(e))



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


def validate_email(email):
    email_validator = EmailValidator()
    try:
        email_validator(email)
    except ValidationError:
        return False
    return True
