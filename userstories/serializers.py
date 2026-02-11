# # # userstories/serializers.py
# # from rest_framework import serializers
# # from .models import UserStory

# # class UserStorySerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = UserStory
# #         fields = "__all__"


# from rest_framework import serializers
# from .models import UserStory
# from projects.models import Project


# class UserStorySerializer(serializers.ModelSerializer):
#     project_slug = serializers.CharField(write_only=True)

#     class Meta:
#         model = UserStory
#         fields = [
#             "id",
#             "ref",
#             "subject",
#             "description",
#             "status",
#             "project",
#             "project_slug",
#             "created_at",
#         ]
#         read_only_fields = ["project"]

#     def create(self, validated_data):
#         project_slug = validated_data.pop("project_slug")
#         project = Project.objects.get(slug=project_slug)
#         validated_data["project"] = project
#         return super().create(validated_data)

from rest_framework import serializers
from django.db.models import Max
from .models import UserStory
from projects.models import Project


class UserStorySerializer(serializers.ModelSerializer):
    project_slug = serializers.CharField(write_only=True)

    class Meta:
        model = UserStory
        fields = [
            "id",
            "ref",
            "subject",
            "description",
            "status",
            "project",
            "sprint",
            "project_slug",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "ref",
            "project",
            "created_at",
        ]

    def create(self, validated_data):
        project_slug = validated_data.pop("project_slug")
        project = Project.objects.get(slug=project_slug)

        # 🔢 Get next ref PER PROJECT
        last_ref = (
            UserStory.objects
            .filter(project=project)
            .aggregate(max_ref=Max("ref"))["max_ref"]
            or 0
        )

        validated_data["project"] = project
        validated_data["ref"] = last_ref + 1  # ✅ FIX

        return super().create(validated_data)
