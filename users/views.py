# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework.permissions import IsAuthenticated

# # from .serializers import UserSerializer


# # class MeView(APIView):
# #     permission_classes = [IsAuthenticated]

# #     def get(self, request):
# #         serializer = UserSerializer(request.user)
# #         return Response(serializer.data)

# from django.contrib.auth.models import User
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from rest_framework.permissions import IsAuthenticated
# from .serializers import UserSerializer

# class MeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)


# class SignupView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get("username")
#         email = request.data.get("email")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response(
#                 {"error": "Username and password required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if User.objects.filter(username=username).exists():
#             return Response(
#                 {"error": "Username already exists"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )

#         return Response(
#             {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email
#             },
#             status=status.HTTP_201_CREATED
#         )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import UserSerializer, SignupSerializer,UserListSerializer
from rest_framework.generics import ListAPIView
from core.permissions import IsPM
from core.permissions import IsPMOrManager


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsPMOrManager]  # Only PM can see all users

    def get_queryset(self):
        return User.objects.all().order_by("id")
