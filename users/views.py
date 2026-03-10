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
import requests as http_requests
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer, SignupSerializer,UserListSerializer
from rest_framework.generics import ListAPIView
from core.permissions import IsPM
from core.permissions import IsPMOrManager
from .models import UserRoles
from .serializers import AssignRolesSerializer
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class SignupView(APIView):


    permission_classes = [IsAuthenticated, IsPM]

    def post(self, request):

        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # permission_classes = [AllowAny]

    # def post(self, request):
    #     serializer = SignupSerializer(data=request.data)

    #     if serializer.is_valid():
    #         user = serializer.save()
    #         return Response(
    #             UserSerializer(user).data,
    #             status=status.HTTP_201_CREATED
    #         )

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsPMOrManager]  # Only PM can see all users

    def get_queryset(self):
        return User.objects.all().order_by("id")
    
class AssignUserRolesView(APIView):
    permission_classes = [IsAuthenticated, IsPMOrManager]

    def post(self, request, user_id):

        serializer = AssignRolesSerializer(data=request.data)

        if serializer.is_valid():

            roles = serializer.validated_data["roles"]

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # remove existing roles
            UserRoles.objects.filter(user=user).delete()

            # create new roles
            for role in roles:
                UserRoles.objects.create(user=user, role=role)

            return Response(
                {
                    "user_id": user.id,
                    "roles": roles
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




class MicrosoftLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ms_token = request.data.get('access_token')
        if not ms_token:
            return Response({'error': 'access_token is required'}, status=400)

        # Verify token with Microsoft Graph
        graph_response = http_requests.get(
            'https://graph.microsoft.com/v1.0/me',
            headers={'Authorization': f'Bearer {ms_token}'}
        )

        if graph_response.status_code != 200:
            return Response({'error': 'Invalid Microsoft token'}, status=401)

        ms_user = graph_response.json()
        email = ms_user.get('mail') or ms_user.get('userPrincipalName')
        username = ms_user.get('displayName', '').replace(' ', '_').lower()

        if not email:
            return Response({'error': 'Could not retrieve email from Microsoft'}, status=400)

        # Find or create the user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username or email.split('@')[0],
                'is_active': True,
                'role': 'DEV',  # default role — change as needed
            }
        )

        # Issue your app's JWT — same as regular login
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': getattr(user, 'role', None),
                'is_superuser': user.is_superuser,
            },
            'created': created,
        })