from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

from .models import TimeLog
from .serializers import TimeLogSerializer
from core.permissions import IsManager, IsPMOrManager


class TimeLogViewSet(ModelViewSet):
    serializer_class = TimeLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = TimeLog.objects.select_related(
            "user", "project", "sprint", "task"
        )

        if user.is_superuser:
            pass
        elif IsPMOrManager().has_permission(self.request, self):
            # PM or MGR sees all logs in projects they are members of
            queryset = queryset.filter(
                project__members__user=user
            ).distinct()
        else:
            # Everyone else sees only their own logs
            queryset = queryset.filter(user=user)

        # Optional filters via query params
        task_id = self.request.query_params.get("task")
        project_id = self.request.query_params.get("project")
        sprint_id = self.request.query_params.get("sprint")
        date = self.request.query_params.get("date")

        if task_id:
            queryset = queryset.filter(task_id=task_id)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if sprint_id:
            queryset = queryset.filter(sprint_id=sprint_id)
        if date:
            queryset = queryset.filter(date=date)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        log = self.get_object()
        if not (
            self.request.user.is_superuser
            or IsPMOrManager().has_permission(self.request, self)
            or log.user == self.request.user
        ):
            raise PermissionDenied("You can only edit your own time logs.")
        serializer.save()

    def perform_destroy(self, instance):
        if not (
            self.request.user.is_superuser
            or IsPMOrManager().has_permission(self.request, self)
            or instance.user == self.request.user
        ):
            raise PermissionDenied("You can only delete your own time logs.")
        instance.delete()

    @action(detail=False, methods=["get"], url_path="my")
    def my_logs(self, request):
        queryset = TimeLog.objects.filter(
            user=request.user
        ).select_related("project", "sprint", "task").order_by("-date")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="task-summary")
    def task_summary(self, request):
        task_id = request.query_params.get("task")
        if not task_id:
            return Response({"detail": "task query param required."}, status=400)

        summary = (
            TimeLog.objects.filter(task_id=task_id)
            .values("user__id", "user__username")
            .annotate(total_hours=Sum("worked_hours"))
            .order_by("-total_hours")
        )
        return Response(summary)