from rest_framework import views, response, exceptions, permissions,status, serializers
from utils.api_response import CustomResponse 
from apps.users import authentication
import jwt
from django.conf import settings

from .services import user_services
#Importar Allow
from . import serializer as user_serializer


class RegisterApi(views.APIView):
    def post(self, request):
        new_user = request.data
        password = new_user.get("password")
        password_confirmation = new_user.get("password_confirmation")

        try:
            if password != password_confirmation:
                raise exceptions.ValidationError("Passwords do not match")
        except exceptions.ValidationError as e:
            error_message = {
                "error": "{}".format(e.args[0]) 
            }# Personalizar el mensaje de error
            
            # Utilizar CustomResponse para construir la respuesta de error
            return CustomResponse(
                data=None,
                status=status.HTTP_400_BAD_REQUEST,
                message="Validation error",
                error=error_message
            )

        try:
            serializer = user_serializer.UserSerializer(data=new_user)
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:

            error_message = {
                "error": "The following fields are required: {}".format(", ".join(e.args[0].keys()))  
            }

            return CustomResponse(
                data=None,
                status=status.HTTP_400_BAD_REQUEST,
                message="Validation error",
                error=error_message
            )
        
        data = serializer.validated_data    
        #we pass the user data to the service so that it is created via dataclass
        user_services.instance = user_services.create_user(user_dc=data)
        
        return CustomResponse(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            message="User created successfully",
        )
        
class LoginApi(views.APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        user = user_services.user_email_selector(email=email)
        print("UserPerro")
        print(user)

        try:
            if not user:
                raise exceptions.AuthenticationFailed("User not found")
        except exceptions.AuthenticationFailed as e:
            error_message = {
                "error": "{}".format(e.args[0]) 
            }
            return CustomResponse(
                data=None,
                status=status.HTTP_404_NOT_FOUND,
                message="User not found",
                error=error_message
            )
        print("pasamos primer try")
        try:

            if not user.check_password(password):
                raise exceptions.AuthenticationFailed("Incorrect password")
        except exceptions.AuthenticationFailed as e:
            error_message = {
                "error": "{}".format(e.args[0]) 
            }
            return CustomResponse(
                data=None,
                status=status.HTTP_401_UNAUTHORIZED,
                message="Incorrect password",
                error=error_message
            )
        
        token = user_services.create_token(user_id=user.id)
        print(token)

        # Crear un diccionario con los datos de respuesta, incluyendo el token
        response_data = {
            "token": token
        }

        # Pasar el diccionario como argumento a tu CustomResponse
        return CustomResponse(
            data=response_data,
            status=status.HTTP_200_OK,
            message="Login successful"
        )
    
class UserApi(views.APIView):
    """
    This endpoint can only be used
    if the user is authenticated
    """

    #using personalized authentication, remember to put a comma so that it reads the tuple correctly
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = request.user

        serializer = user_serializer.UserSerializer(user)

        return response.Response(serializer.data)
    

class LogoutApi(views.APIView):
    authentication_classes = (authentication.CustomUserAuthentication,)
    # Aquí puedes agregar otras clases de permisos si es necesario
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # Obtén el token JWT de la cabecera de autorización
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header is None:
            return CustomResponse(
                data=None,
                status=status.HTTP_401_UNAUTHORIZED,
                message="No authorization token provided",   
            )

        # Extraer el token de autorización del encabezado
        auth_token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header

        # Realiza cualquier verificación adicional que necesites con el token JWT

        # Elimina el token JWT en el backend
        try:
            # Verifica el token JWT para obtener la información del usuario
            payload = jwt.decode(auth_token, settings.JWT_SECRET, algorithms=["HS256"])
            user_id = payload["id"]

            # Invalida el token JWT en el backend agregándolo a la lista negra
            # Puedes almacenar la lista negra en una base de datos, en memoria, o en cualquier otro lugar
            # Aquí se muestra un ejemplo de cómo almacenar la lista negra en una variable de clase en la vista
            self.authentication_classes.blacklist.append(auth_token)

            # Elimina la cookie (si es necesario)
            response = CustomResponse(
                data=None,
                status=status.HTTP_200_OK,
                message="Logout successful"
            )
            
            response.delete_cookie(key="jwt")
            return response

        except jwt.ExpiredSignatureError:
            return CustomResponse(
                data=None,
                status=status.HTTP_401_UNAUTHORIZED,
                message="Token has expired"
            )
        except jwt.InvalidTokenError:
            return CustomResponse(
                data=None,
                status=status.HTTP_401_UNAUTHORIZED,
                message="Invalid token"
            )






















