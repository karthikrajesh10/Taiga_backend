# from django.shortcuts import render

# # Create your views here.

# userstories/views.py
# from rest_framework.viewsets import ModelViewSet
# from .models import UserStory
# from .serializers import UserStorySerializer

# # class UserStoryViewSet(ModelViewSet):
# #     queryset = UserStory.objects.all()
# #     serializer_class = UserStorySerializer

# from rest_framework.permissions import IsAuthenticated

# class UserStoryViewSet(ModelViewSet):
#     serializer_class = UserStorySerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         queryset = UserStory.objects.all()
#         project_id = self.request.query_params.get("project")

#         if project_id:
#             queryset = queryset.filter(project_id=project_id)

#         return queryset

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import UserStory
from .serializers import UserStorySerializer
from core.permissions import IsManager


class UserStoryViewSet(ModelViewSet):
    serializer_class = UserStorySerializer
    permission_classes = [IsAuthenticated]

   
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
        #if self.action == "create":
            return [IsAuthenticated(), IsManager()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = UserStory.objects.all()
        else:
            queryset = UserStory.objects.filter(
                project__members__user=user
            ).distinct()

        # Filter by project slug
        project_slug = self.request.query_params.get("project_slug")
        if project_slug:
            queryset = queryset.filter(project__slug=project_slug)

        # Backlog filter
        sprint_isnull = self.request.query_params.get("sprint_isnull")
        if sprint_isnull == "true":
            queryset = queryset.filter(sprint__isnull=True)

        # Specific sprint
        sprint_id = self.request.query_params.get("sprint")
        if sprint_id:
            queryset = queryset.filter(sprint_id=sprint_id)

        return queryset
