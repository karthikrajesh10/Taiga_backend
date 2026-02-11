# # # from django.shortcuts import render

# # # # Create your views here.

# # # tasks/views.py
# # from rest_framework.viewsets import ModelViewSet
# # from .models import Task
# # from .serializers import TaskSerializer

# # class TaskViewSet(ModelViewSet):
# #     queryset = Task.objects.all()
# #     serializer_class = TaskSerializer

# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated
# from django.db.models import Max

# from .models import Task
# from .serializers import TaskSerializer


# class TaskViewSet(ModelViewSet):
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         queryset = Task.objects.all()

#         project_slug = self.request.query_params.get("project__slug")
#         userstory = self.request.query_params.get("userstory")

#         if project_slug:
#             queryset = queryset.filter(project__slug=project_slug)

#         if userstory:
#             queryset = queryset.filter(userstory=userstory)

#         return queryset

#     def perform_create(self, serializer):
#         project = serializer.validated_data["project"]

#         last_ref = (
#             Task.objects
#             .filter(project=project)
#             .aggregate(Max("ref"))["ref__max"]
#             or 0
#         )

#         serializer.save(
#             ref=last_ref + 1,
#             created_by=self.request.user
#         )

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Max
from .models import Task
from .serializers import TaskSerializer
from projects.models import Project

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.all()

        project_slug = self.request.query_params.get("project__slug")
        if project_slug:
            queryset = queryset.filter(project__slug=project_slug)

        userstory_id = self.request.query_params.get("userstory")
        if userstory_id:
            queryset = queryset.filter(userstory_id=userstory_id)

        return queryset

    def perform_create(self, serializer):
        project_slug = serializer.validated_data.pop("project_slug")
        project = Project.objects.get(slug=project_slug)

        last_ref = (
            Task.objects
            .filter(project=project)
            .aggregate(Max("ref"))["ref__max"]
            or 0
        )

        serializer.save(
            project=project,
            ref=last_ref + 1,
            created_by=self.request.user
        )

