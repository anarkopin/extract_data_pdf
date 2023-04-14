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
    from ..models import Rol


#in this way we transform the dictionary of user that we receive into a class
@dataclasses.dataclass
class RolDataClass:
    rol: str

    @classmethod
    def from_instance(cls, rol: "Rol") -> "RolDataClass":
        return cls(
            rol=rol.rol,
            id=rol.id,
        )
    

def create_rol(rol_dc: "RolDataClass") -> "RolDataClass":
    #validación de entrada
    if not rol_dc.rol:
        raise ValueError("Rol is required field")

    instance = models.Rol(
        rol=rol_dc.rol,
    )

    try:
        instance.save()
    except IntegrityError as e:
        raise ValueError("Rol already exists")    

    return RolDataClass.from_instance(instance)

