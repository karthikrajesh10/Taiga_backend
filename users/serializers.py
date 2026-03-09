# from django.contrib.auth.models import User
# from rest_framework import serializers


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             "id",
#             "username",
#             "email",
#             "is_staff",
#             "is_superuser",
#         ]

from rest_framework import serializers
from .models import User
from .models import UserRoles


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "employee_id",
            "company_name",
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
        ]
        read_only_fields = ["id", "is_staff", "is_superuser", "created_at"]


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "employee_id",
            "company_name",
            "role",
        ]

    def create(self, validated_data):

        employee_id = validated_data.get("employee_id")
        if not employee_id:  # handles "", None, or other falsy values
            validated_data["employee_id"] = None
        company_name = validated_data.get("company_name")
        if not company_name:
            validated_data["company_name"] = None
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserListSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "username", "email", "role","roles"]
    def get_roles(self, obj):
        # get roles from UserRoles table
        return list(
            obj.user_roles.values_list("role", flat=True)
        )


from .models import UserRoles


class AssignRolesSerializer(serializers.Serializer):
    roles = serializers.ListField(
        child=serializers.ChoiceField(choices=UserRoles.ROLE_CHOICES)
    )

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user info to response
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "role": getattr(self.user, "role", None),
            "is_superuser": self.user.is_superuser,
        }

        return data