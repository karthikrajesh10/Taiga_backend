# # # # from django.shortcuts import render

# # # # # Create your views here.

# # # # tasks/views.py
# # # from rest_framework.viewsets import ModelViewSet
# # # from .models import Task
# # # from .serializers import TaskSerializer

# # # class TaskViewSet(ModelViewSet):
# # #     queryset = Task.objects.all()
# # #     serializer_class = TaskSerializer

# # from rest_framework.viewsets import ModelViewSet
# # from rest_framework.permissions import IsAuthenticated
# # from django.db.models import Max

# # from .models import Task
# # from .serializers import TaskSerializer


# # class TaskViewSet(ModelViewSet):
# #     serializer_class = TaskSerializer
# #     permission_classes = [IsAuthenticated]

# #     def get_queryset(self):
# #         queryset = Task.objects.all()

# #         project_slug = self.request.query_params.get("project__slug")
# #         userstory = self.request.query_params.get("userstory")

# #         if project_slug:
# #             queryset = queryset.filter(project__slug=project_slug)

# #         if userstory:
# #             queryset = queryset.filter(userstory=userstory)

# #         return queryset

# #     def perform_create(self, serializer):
# #         project = serializer.validated_data["project"]

# #         last_ref = (
# #             Task.objects
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
# from .models import Task
# from .serializers import TaskSerializer
# from projects.models import Project

# class TaskViewSet(ModelViewSet):
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         queryset = Task.objects.all()

#         project_slug = self.request.query_params.get("project__slug")
#         if project_slug:
#             queryset = queryset.filter(project__slug=project_slug)

#         userstory_id = self.request.query_params.get("userstory")
#         if userstory_id:
#             queryset = queryset.filter(userstory_id=userstory_id)

#         return queryset

#     def perform_create(self, serializer):
#         project_slug = serializer.validated_data.pop("project_slug")
#         project = Project.objects.get(slug=project_slug)

#         last_ref = (
#             Task.objects
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
from .models import Task
from .serializers import TaskSerializer
from core.permissions import IsManager
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     queryset = Task.objects.all()

    #     # Filter by user story
    #     user_story_id = self.request.query_params.get("user_story")
    #     if user_story_id:
    #         queryset = queryset.filter(user_story_id=user_story_id)

    #     return queryset
    def get_permissions(self):
        if self.action in ["create", "destroy"]:
        
        #if self.action == "create":
            return [IsAuthenticated(), IsManager()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = Task.objects.all()
        else:
            queryset = Task.objects.filter(
                user_story__project__members__user=user
            ).distinct()

        user_story_id = self.request.query_params.get("user_story")
        if user_story_id:
            queryset = queryset.filter(user_story_id=user_story_id)

        return queryset

    def perform_update(self, serializer):
        user = self.request.user

        # if user.role not in ["DEV", "MGR"]:
        #     raise PermissionDenied("You cannot modify tasks")
        if not (user.is_superuser or user.role in ["DEV", "MGR"]):
            raise PermissionDenied("You cannot modify tasks")

        serializer.save()
    # def destroy(self, request, *args, **kwargs):
    #     user = request.user

    #     # Only  MGR or superuser can delete
    #     #if not (user.is_superuser or user.role =="MGR" ):
    #     if not (user.is_superuser or user.role in ["DEV", "MGR"]):

    #         raise PermissionDenied("You cannot delete this task")

    #     return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="my")
    def my_tasks(self, request):
        user = request.user

        queryset = Task.objects.filter(
            assignee=user
        ).select_related("user_story")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        

