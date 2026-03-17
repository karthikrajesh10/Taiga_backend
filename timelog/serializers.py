from rest_framework import serializers
from .models import TimeLog


class TimeLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = TimeLog
        fields = [
            "id",
            "user",
            "username",
            "project",
            "sprint",
            "task",
            "date",
            "worked_hours",
            "comment",
            "created_at",
        ]
        read_only_fields = ["id", "user", "username", "created_at"]

    def validate_worked_hours(self, value):
        if value <= 0:
            raise serializers.ValidationError("Worked hours must be greater than 0.")
        if value > 24:
            raise serializers.ValidationError("Worked hours cannot exceed 24 in a day.")
        return value

    def validate(self, attrs):
        # If task is provided, auto-fill project and sprint from it
        task = attrs.get("task")
        if task:
            if not attrs.get("project") and task.user_story.project:
                attrs["project"] = task.user_story.project
            if not attrs.get("sprint") and task.user_story.sprint_set.exists():
                attrs["sprint"] = task.user_story.sprint_set.first()
        return attrs