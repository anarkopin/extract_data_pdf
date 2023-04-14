from django.conf import settings
from rest_framework import authentication, exceptions
import jwt

from . import models 

#Authentication class to cookies
class CustomUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header is None:
            return None

        # Extraer el token de la cabecera de autorización
        auth_token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header

        try:
            payload = jwt.decode(auth_token, settings.JWT_SECRET, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token de autorización expirado")
        except jwt.exceptions.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Token de autorización inválido")

        user = models.User.objects.filter(id=payload["id"]).first()

        return (user, None)