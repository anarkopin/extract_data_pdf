from django.http import JsonResponse
from rest_framework import views, response, exceptions, permissions,status
#Importar Allow

from . import serializer as user_serializer
from . import services, authentication

class RegisterApi(views.APIView):
    def post(self, request):
        new_user = request.data
        password = new_user.get("password")
        password_confirmation = new_user.get("password_confirmation")

        if password != password_confirmation:
            raise exceptions.ValidationError("Passwords do not match")

        serializer = user_serializer.UserSerializer(data=new_user)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data    

        #we pass the user data to the service so that it is created via dataclass
        services.instance = services.create_user(user_dc=data)
        
        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
class LoginApi(views.APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        user = services.user_email_selector(email=email)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        
        # if not user.is_email_verified:
        #     raise exceptions.AuthenticationFailed("Email is not verified, please check your email")
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")
        
        token = services.create_token(user_id=user.id)

        resp = JsonResponse({'token': token})
        
        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp
    
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
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        resp = response.Response()

        resp.delete_cookie(key="jwt")

        resp.data = {
            "message": "success"
        }

        return resp

        






















