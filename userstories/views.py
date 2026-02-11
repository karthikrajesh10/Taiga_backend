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


class UserStoryViewSet(ModelViewSet):
    serializer_class = UserStorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = UserStory.objects.all()

        # Filter by project ID (optional)
        project_id = self.request.query_params.get("project")
        
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        

        # Filter by project slug (recommended for frontend)
        project_slug = self.request.query_params.get("project__slug")
        if project_slug:
            queryset = queryset.filter(project__slug=project_slug)

        sprint_id = self.request.query_params.get("sprint")
        sprint_isnull = self.request.query_params.get("sprint__isnull")

        # if sprint_id == "null":
        #     queryset = queryset.filter(sprint__isnull=True)

        # # Sprint stories
        # elif sprint_id:
        #     queryset = queryset.filter(sprint_id=sprint_id)
        if sprint_isnull == "true":
            queryset = queryset.filter(sprint__isnull=True)

    # Sprint stories
        elif sprint_id:
            queryset = queryset.filter(sprint_id=sprint_id)

        return queryset
