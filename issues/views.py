# # # from django.shortcuts import render

# # # # Create your views here.

# # # issues/views.py
# # from rest_framework.viewsets import ModelViewSet
# # from .models import Issue
# # from .serializers import IssueSerializer

# # class IssueViewSet(ModelViewSet):
# #     queryset = Issue.objects.all()
# #     serializer_class = IssueSerializer


# # from rest_framework.viewsets import ModelViewSet
# # from rest_framework.permissions import IsAuthenticated
# # from django.db.models import Max

# # from .models import Issue
# # from .serializers import IssueSerializer

# # class IssueViewSet(ModelViewSet):
# #     serializer_class = IssueSerializer
# #     permission_classes = [IsAuthenticated]

# #     def get_queryset(self):
# #         queryset = Issue.objects.all()

# #         project_slug = self.request.query_params.get("project__slug")
# #         if project_slug:
# #             queryset = queryset.filter(project__slug=project_slug)

# #         return queryset

# #     def perform_create(self, serializer):
# #         project = serializer.validated_data["project"]

# #         last_ref = (
# #             Issue.objects
# #             .filter(project=project)
# #             .aggregate(Max("ref"))["ref__max"]
# #             or 0
# #         )

# #         serializer.save(
# #             ref=last_ref + 1,
# #             created_by=self.request.user
# #         )

# # class IssueViewSet(ModelViewSet):
# #     serializer_class = IssueSerializer
# #     permission_classes = [IsAuthenticated]

# #     def get_queryset(self):
# #         queryset = Issue.objects.all()
# #         project_slug = self.request.query_params.get("project__slug")
# #         if project_slug:
# #             queryset = queryset.filter(project__slug=project_slug)
# #         return queryset

# #     def get_serializer_context(self):
# #         context = super().get_serializer_context()
# #         context["request"] = self.request
# #         return context

# #     def perform_create(self, serializer):
# #         project = serializer.validated_data["project"]

# #         last_ref = (
# #             Issue.objects
# #             .filter(project=project)
# #             .aggregate(Max("ref"))["ref__max"]
# #             or 0
# #         )

# #         serializer.save(
# #             ref=last_ref + 1,
# #             created_by=self.request.user
# #         )
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated
# from django.db.models import Max

# from .models import Issue
# from .serializers import IssueSerializer

# class IssueViewSet(ModelViewSet):
#     serializer_class = IssueSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         queryset = Issue.objects.all()

#         project_slug = self.request.query_params.get("project__slug")
#         if project_slug:
#             queryset = queryset.filter(project__slug=project_slug)

#         return queryset

#     def perform_create(self, serializer):
#         project = serializer.validated_data.get("project")

#         last_ref = (
#             Issue.objects
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
from django.db import transaction
from django.db.models import Max
from projects.models import Project

from .models import Issue
from .serializers import IssueSerializer


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_slug = self.request.query_params.get("project__slug")
        if project_slug:
            queryset = queryset.filter(project__slug=project_slug)
        return queryset

    @transaction.atomic
    def perform_create(self, serializer):
        # ✅ READ slug (this EXISTS)
        project_slug = serializer.validated_data.pop("project_slug")

        # ✅ Resolve project HERE
        project = Project.objects.select_for_update().get(slug=project_slug)

        # 🔒 Atomic ref generation
        last_ref = (
            Issue.objects
            .select_for_update()
            .filter(project=project)
            .aggregate(Max("ref"))["ref__max"]
            or 0
        )

        serializer.save(
            project=project,
            ref=last_ref + 1,
            created_by=self.request.user
        )
