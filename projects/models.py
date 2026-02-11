# from django.db import models

# class Project(models.Model):
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True)
#     description = models.TextField(blank=True)
#     created_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Project(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("member", "Member"),
        ("viewer", "Viewer"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="project_memberships",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="member",
    )
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "project")

    def __str__(self):
        return f"{self.user} → {self.project} ({self.role})"
