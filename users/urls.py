from django.urls import path
from .views import MeView, SignupView,UserListView

urlpatterns = [
    path("me/", MeView.as_view(), name="users-me"),
    path("signup/", SignupView.as_view(), name="users-signup"),
    path("", UserListView.as_view(), name="users-list"),
]
