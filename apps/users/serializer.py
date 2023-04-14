from rest_framework import serializers

from .services import user_services



class RolSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    rol = serializers.CharField()

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return user_services.RolDataClass(**data)

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    rol = serializers.CharField()

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return user_services.UserDataClass(**data)
