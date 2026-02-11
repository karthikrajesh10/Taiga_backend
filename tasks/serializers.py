# # # tasks/serializers.py
# # from rest_framework import serializers
# # from .models import Task

# # class TaskSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Task
# #         fields = "__all__"

# from rest_framework import serializers
# from .models import Task
# from projects.models import Project


# class TaskSerializer(serializers.ModelSerializer):
#     project_slug = serializers.CharField(write_only=True)
#     created_by_username = serializers.CharField(
#         source="created_by.username",
#         read_only=True
#     )
#     assigned_to_username = serializers.CharField(
#         source="assigned_to.username",
#         read_only=True
#     )

#     class Meta:
#         model = Task
#         fields = [
#             "id",
#             "ref",
#             "subject",
#             "description",
#             "status",
#             "project",
#             "project_slug",
#             "userstory",
#             "created_by",
#             "created_by_username",
#             "assigned_to",
#             "assigned_to_username",
#             "created_at",
#             "modified_at",
#         ]
#         read_only_fields = [
#             "id",
#             "ref",
#             "project",
#             "created_by",
#             "created_at",
#             "modified_at",
#         ]

#     def create(self, validated_data):
#         project_slug = validated_data.pop("project_slug")
#         project = Project.objects.get(slug=project_slug)
#         validated_data["project"] = project
#         return super().create(validated_data)

from rest_framework import serializers
from django.db.models import Max
from .models import Task
from projects.models import Project

class TaskSerializer(serializers.ModelSerializer):
    project_slug = serializers.CharField(write_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "ref",
            "subject",
            "description",
            "status",
            "project",
            "project_slug",
            "userstory",
            "created_by",
            "assigned_to",
            "created_at",
            "modified_at",
        ]
        read_only_fields = [
            "id",
            "ref",
            "project",
            "created_by",
            "created_at",
            "modified_at",
        ]

    # def create(self, validated_data):
    #     project_slug = validated_data.pop("project_slug")
    #     project = Project.objects.get(slug=project_slug)

    #     validated_data["project"] = project
    #     return super().create(validated_data)
