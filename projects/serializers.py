# from rest_framework import serializers
# from .models import Project

# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = "__all__"

from rest_framework import serializers
from .models import Project, ProjectMembership



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["created_date"]

    def create(self, validated_data):
        request = self.context["request"]

        project = super().create(validated_data)

        # 🔑 Add creator as OWNER
        ProjectMembership.objects.create(
            user=request.user,
            project=project,
            role="owner",
        )

        return project

from django.contrib.auth.models import User


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ProjectMembershipSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    user = UserMiniSerializer(read_only=True)

    class Meta:
        model = ProjectMembership
        fields = [
            "id",
            "project",
            "user",
            "user_email",
            "role",
            "is_active",
        ]
        read_only_fields = ["id", "user"]

    def create(self, validated_data):
        from django.contrib.auth.models import User

        user_email = validated_data.pop("user_email")
        project = validated_data["project"]

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"user_email": "User with this email does not exist"}
            )

        validated_data["user"] = user
        return super().create(validated_data)
