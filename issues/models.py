# # from django.db import models

# # # Create your models here.
# # from django.db import models
# # from projects.models import Project

# # class Issue(models.Model):
# #     subject = models.CharField(max_length=300)
# #     project = models.ForeignKey(Project, on_delete=models.CASCADE)

# #     def __str__(self):
# #         return self.subject

# from django.db import models
# from projects.models import Project
# from django.conf import settings

# class Issue(models.Model):
#     ISSUE_TYPES = [
#         ("bug", "Bug"),
#         ("question", "Question"),
#         ("enhancement", "Enhancement"),
#     ]

#     SEVERITY_CHOICES = [
#         ("wishlist", "Wishlist"),
#         ("minor", "Minor"),
#         ("normal", "Normal"),
#         ("important", "Important"),
#         ("critical", "Critical"),
#     ]

#     PRIORITY_CHOICES = [
#         ("low", "Low"),
#         ("normal", "Normal"),
#         ("high", "High"),
#     ]

#     STATUS_CHOICES = [
#         ("new", "New"),
#         ("in_progress", "In Progress"),
#         ("ready_for_test", "Ready for Test"),
#         ("closed", "Closed"),
#     ]

#     project = models.ForeignKey(
#         Project,
#         on_delete=models.CASCADE,
#         related_name="issues"
#     )

#     ref = models.PositiveIntegerField()
#     subject = models.CharField(max_length=255)
#     description = models.TextField(blank=True)

#     type = models.CharField(
#         max_length=20,
#         choices=ISSUE_TYPES,
#         default="bug"
#     )

#     severity = models.CharField(
#         max_length=20,
#         choices=SEVERITY_CHOICES,
#         default="normal"
#     )

#     priority = models.CharField(
#         max_length=20,
#         choices=PRIORITY_CHOICES,
#         default="normal"
#     )

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default="new"
#     )

#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name="created_issues"
#     )

#     assigned_to = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name="assigned_issues"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["-modified_at"]
#         unique_together = ("project", "ref")

#     def __str__(self):
#         return f"#{self.ref} {self.subject}"

# from django.db import models
# from django.utils import timezone
# from projects.models import Project

# class Issue(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)

#     ref = models.PositiveIntegerField(editable=False)

#     subject = models.CharField(max_length=255)
#     description = models.TextField(blank=True)

#     type = models.CharField(max_length=20, default="bug")
#     severity = models.CharField(max_length=20, default="normal")
#     priority = models.CharField(max_length=20, default="normal")
#     status = models.CharField(max_length=20, default="New")

#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         if not self.ref:
#             last_ref = (
#                 Issue.objects.filter(project=self.project)
#                 .aggregate(models.Max("ref"))["ref__max"]
#             )
#             self.ref = (last_ref or 0) + 1
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"#{self.ref} {self.subject}"

from django.db import models
from projects.models import Project
from django.contrib.auth.models import User

class Issue(models.Model):
    ref = models.PositiveIntegerField()
    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    type = models.CharField(max_length=50)
    severity = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="New")

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_issues"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("project", "ref")
        ordering = ["ref"]

    def __str__(self):
        return f"#{self.ref} {self.subject}"
