# # from rest_framework import serializers
# # from .models import Sprint


# # class SprintSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Sprint
# #         fields = "__all__"

# from rest_framework import serializers
# from .models import Sprint
# from projects.models import Project

# class SprintSerializer(serializers.ModelSerializer):
#     project_slug = serializers.CharField(write_only=True)

#     class Meta:
#         model = Sprint
#         fields = [
#             "id",
#             "name",
#             "project",
#             "project_slug",
#             "start_date",
#             "end_date",
#             "is_active",
#             "created_at",
#         ]
#         read_only_fields = ["id", "project", "created_at"]

#     def create(self, validated_data):
#         project_slug = validated_data.pop("project_slug")
#         project = Project.objects.get(slug=project_slug)

#         validated_data["project"] = project
#         return super().create(validated_data)

from rest_framework import serializers
from .models import Sprint
from projects.models import Project

class SprintSerializer(serializers.ModelSerializer):
    project_slug = serializers.CharField(write_only=True)

    class Meta:
        model = Sprint
        fields = [
            "id",
            "name",
            "project",
            "project_slug",
            "start_date",
            "end_date",
            "is_active",
            "created_at",
            
        ]
        read_only_fields = ["id", "project", "created_at"]

    def create(self, validated_data):
        project_slug = validated_data.pop("project_slug")
        project = Project.objects.get(slug=project_slug)

        validated_data["project"] = project
        return super().create(validated_data)
