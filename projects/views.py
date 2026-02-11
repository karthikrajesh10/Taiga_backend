# # from django.shortcuts import render

# # # Create your views here.
# from rest_framework.viewsets import ModelViewSet
# from .models import Project
# from .serializers import ProjectSerializer

# class ProjectViewSet(ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Superusers can see everything (optional but useful)
        if user.is_superuser:
            return Project.objects.all()

        # Only projects where user is a member
        return Project.objects.filter(
            memberships__user=user,
            memberships__is_active=True,
        ).distinct()

from rest_framework.exceptions import PermissionDenied
from .models import ProjectMembership
from .serializers import ProjectMembershipSerializer



class ProjectMembershipViewSet(ModelViewSet):
    serializer_class = ProjectMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # project_id = self.request.query_params.get("project")

        # queryset = ProjectMembership.objects.select_related("user", "project")

        # # 🔐 Non-superusers only see projects they belong to
        # if not user.is_superuser:
        #     queryset = queryset.filter(
        #         project__memberships__user=user,
        #         project__memberships__is_active=True,
        #     )

        # # 🎯 CRITICAL FIX: filter by project if provided
        # if project_id:
        #     queryset = queryset.filter(project_id=project_id)

        # return queryset

        if user.is_superuser:
            return ProjectMembership.objects.all()

        return ProjectMembership.objects.filter(
            project__memberships__user=user,
            project__memberships__is_active=True,
        )

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        user = self.request.user

        # 🔐 Only OWNER can add members (Taiga rule)
        if not ProjectMembership.objects.filter(
            project=project,
            user=user,
            role="owner",
            is_active=True,
        ).exists():
            raise PermissionDenied("Only project owners can add members")

        serializer.save()
