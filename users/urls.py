from django.urls import path
from .views import MeView, SignupView,UserListView,AssignUserRolesView,MicrosoftLoginView

urlpatterns = [
    path("me/", MeView.as_view(), name="users-me"),
    path("signup/", SignupView.as_view(), name="users-signup"),
    path("", UserListView.as_view(), name="users-list"),
    path("<int:user_id>/roles/", AssignUserRolesView.as_view(), name="assign-roles"),
    path('auth/microsoft/', MicrosoftLoginView.as_view(), name='microsoft-login'),

]
