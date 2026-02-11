# # from django.shortcuts import render

# # Create your views here.
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated

# from .models import Sprint
# from .serializers import SprintSerializer


# class SprintViewSet(ModelViewSet):
#     queryset = Sprint.objects.all()
#     serializer_class = SprintSerializer
#     permission_classes = [IsAuthenticated]

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Sprint
from .serializers import SprintSerializer

# class SprintViewSet(ModelViewSet):
#     serializer_class = SprintSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         queryset = Sprint.objects.all()

#         project_slug = self.request.query_params.get("project__slug")
#         if project_slug:
#             queryset = queryset.filter(project__slug=project_slug)

#         return queryset

class SprintViewSet(ModelViewSet):
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Sprint.objects.all()

        project_slug = self.request.query_params.get("project_slug")
        if project_slug:
            queryset = queryset.filter(project__slug=project_slug)

        return queryset
