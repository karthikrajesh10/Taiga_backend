# from django.db import models
# from projects.models import Project
# from userstories.models import UserStory

# class Task(models.Model):
#     subject = models.CharField(max_length=300)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     userstory = models.ForeignKey(UserStory, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.subject

from django.db import models
from projects.models import Project
from userstories.models import UserStory
from django.contrib.auth.models import User


class Task(models.Model):
    ref = models.PositiveIntegerField()
    subject = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=50,
        default="New"
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    userstory = models.ForeignKey(
        UserStory,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_tasks"
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("project", "ref")
        ordering = ["ref"]

    def __str__(self):
        return f"#{self.ref} {self.subject}"
