# # # # from django.shortcuts import render

# # # # # Create your views here.

# # # # issues/views.py
# # # from rest_framework.viewsets import ModelViewSet
# # # from .models import Issue
# # # from .serializers import IssueSerializer

# # # class IssueViewSet(ModelViewSet):
# # #     queryset = Issue.objects.all()
# # #     serializer_class = IssueSerializer


# # # from rest_framework.viewsets import ModelViewSet
# # # from rest_framework.permissions import IsAuthenticated
# # # from django.db.models import Max

# # # from .models import Issue
# # # from .serializers import IssueSerializer

# # # class IssueViewSet(ModelViewSet):
# # #     serializer_class = IssueSerializer
# # #     permission_classes = [IsAuthenticated]

# # #     def get_queryset(self):
# # #         queryset = Issue.objects.all()

# # #         project_slug = self.request.query_params.get("project__slug")
# # #         if project_slug:
# # #             queryset = queryset.filter(project__slug=project_slug)

# # #         return queryset

# # #     def perform_create(self, serializer):
# # #         project = serializer.validated_data["project"]

# # #         last_ref = (
# # #             Issue.objects
# # #             .filter(project=project)
# # #             .aggregate(Max("ref"))["ref__max"]
# # #             or 0
# # #         )

# # #         serializer.save(
# # #             ref=last_ref + 1,
# # #             created_by=self.request.user
# # #         )

# # # class IssueViewSet(ModelViewSet):
# # #     serializer_class = IssueSerializer
# # #     permission_classes = [IsAuthenticated]

# # #     def get_queryset(self):
# # #         queryset = Issue.objects.all()
# # #         project_slug = self.request.query_params.get("project__slug")
# # #         if project_slug:
# # #             queryset = queryset.filter(project__slug=project_slug)
# # #         return queryset

# # #     def get_serializer_context(self):
# # #         context = super().get_serializer_context()
# # #         context["request"] = self.request
# # #         return context

# # #     def perform_create(self, serializer):
# # #         project = serializer.validated_data["project"]

# # #         last_ref = (
# # #             Issue.objects
# # #             .filter(project=project)
# # #             .aggregate(Max("ref"))["ref__max"]
# # #             or 0
# # #         )

# # #         serializer.save(
# # #             ref=last_ref + 1,
# # #             created_by=self.request.user
# # #         )
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
# #         project = serializer.validated_data.get("project")

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
# from django.db import transaction
# from django.db.models import Max
# from projects.models import Project

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

#     @transaction.atomic
#     def perform_create(self, serializer):
#         # ✅ READ slug (this EXISTS)
#         project_slug = serializer.validated_data.pop("project_slug")

#         # ✅ Resolve project HERE
#         project = Project.objects.select_for_update().get(slug=project_slug)

#         # 🔒 Atomic ref generation
#         last_ref = (
#             Issue.objects
#             .select_for_update()
#             .filter(project=project)
#             .aggregate(Max("ref"))["ref__max"]
#             or 0
#         )

#         serializer.save(
#             project=project,
#             ref=last_ref + 1,
#             created_by=self.request.user
#         )

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Issue
from .serializers import IssueSerializer
from rest_framework.exceptions import PermissionDenied
# from core.permissions import IsQAOrTestLead



class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     queryset = Issue.objects.all()

    #     # Filter by task
    #     task_id = self.request.query_params.get("task")
    #     if task_id:
    #         queryset = queryset.filter(task_id=task_id)

    #     return queryset
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Issue.objects.all()
        else:
            queryset = Issue.objects.filter(
                task__user_story__project__members__user=user
            ).distinct()

        task_id = self.request.query_params.get("task")
        if task_id:
            queryset = queryset.filter(task_id=task_id)

        return queryset


    def perform_create(self, serializer):
        # serializer.save(created_by=self.request.user)
        user = self.request.user
        issue_type = serializer.validated_data.get("type")

         # if issue_type == "Bug" and not (user.is_superuser or user.role in ["QA", "TL"]):
    #     if issue_type == "Bug":
            # permission = IsQAOrTestLead()
    #       if not permission.has_permission(request, self):
    #           raise PermissionDenied("Only QA or Test Lead can create bugs")
        if issue_type == "Bug" and user.role not in ["QA", "TL"]:
           
            raise PermissionDenied("Only QA or Test Lead can create bugs")

        serializer.save(created_by=user)

    def perform_update(self, serializer):
        user = self.request.user

        # if user.role not in ["QA", "TL","MGR"]:
        #     raise PermissionDenied("Only QA or Test Lead can update issues")
#         permission = IsQAOrTestLead()

#       if not user.is_superuser and not permission.has_permission(request, self):
#           raise PermissionDenied("You cannot modify issue")
        if not (user.is_superuser or user.role in ["QA","TL" ,"MGR"]):
            raise PermissionDenied("You cannot modify issue")

        serializer.save()
    def destroy(self, request, *args, **kwargs):
        user = request.user

        # Only QA, TL, MGR or superuser can delete
#         permission = IsQAOrTestLead()

#       if not user.is_superuser and not permission.has_permission(request, self):
#           raise PermissionDenied("You cannot delete tasks")
        if not (user.is_superuser or user.role in ["QA", "TL", "MGR"]):
            raise PermissionDenied("You cannot delete this issue")

        return super().destroy(request, *args, **kwargs)
        
