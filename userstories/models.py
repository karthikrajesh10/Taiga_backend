# # from django.db import models
# # from projects.models import Project

# # # class UserStory(models.Model):
# # #     subject = models.CharField(max_length=300)
# # #     description = models.TextField(blank=True)
# # #     project = models.ForeignKey(Project, on_delete=models.CASCADE)

# # #     def __str__(self):
# # #         return self.subject

# # class UserStory(models.Model):
# #     STATUS_CHOICES = [
# #         ("New", "New"),
# #         ("Ready", "Ready"),
# #         ("In Progress", "In Progress"),
# #         ("Done", "Done"),
# #     ]

# #     subject = models.CharField(max_length=300)
# #     description = models.TextField(blank=True)
# #     project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name="userstories")

# #     ref = models.PositiveIntegerField(default=0) 

# #     status = models.CharField(
# #         max_length=20,
# #         choices=STATUS_CHOICES,
# #         default="New"
# #     )
# #     points = models.CharField(max_length=10, default="?")

# #     created_at = models.DateTimeField(auto_now_add=True)

# #     sprint = models.ForeignKey(
# #         "sprints.Sprint",
# #         null=True,
# #         blank=True,
# #         on_delete=models.SET_NULL,
# #         related_name="userstories"
# #     )

# #     def __str__(self):
# #         return self.subject


# from django.db import models
# from projects.models import Project


# class UserStory(models.Model):
#     STATUS_CHOICES = [
#         ("New", "New"),
#         ("Ready", "Ready"),
#         ("In Progress", "In Progress"),
#         ("Done", "Done"),
#     ]

#     subject = models.CharField(max_length=300)
#     description = models.TextField(blank=True)

#     project = models.ForeignKey(
#         Project,
#         on_delete=models.CASCADE,
#         related_name="userstories"
#     )

#     sprint = models.ForeignKey(
#         "sprints.Sprint",
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name="userstories"
#     )

#     ref = models.PositiveIntegerField()
#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default="New"
#     )
#     points = models.CharField(max_length=10, default="?")

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["ref"]

#     def __str__(self):
#         return f"#{self.ref} {self.subject}"

from django.db import models
from projects.models import Project
from sprints.models import Sprint
from django.conf import settings


class UserStory(models.Model):

    STATUS_CHOICES = (
        (1, "New"),
        (2, "In Progress"),
        (3, "Ready For Test"),
        (4, "Done"),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="userstories"
    )

    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="userstories"
    )

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, db_index=True)

    description = models.TextField(blank=True)

    priority = models.IntegerField(default=1)

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=1
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_userstories"
    )

    estimated_hours = models.FloatField(null=True, blank=True)
    actual_hours = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["project"]),
            models.Index(fields=["sprint"]),
            models.Index(fields=["status"]),
        ]
    def clean(self):
        if self.pk:
            old = type(self).objects.get(pk=self.pk)
            if self.status < old.status:
                raise ValidationError("Cannot move status backwards")
