# from django.db import models
# from projects.models import Project

# # class UserStory(models.Model):
# #     subject = models.CharField(max_length=300)
# #     description = models.TextField(blank=True)
# #     project = models.ForeignKey(Project, on_delete=models.CASCADE)

# #     def __str__(self):
# #         return self.subject

# class UserStory(models.Model):
#     STATUS_CHOICES = [
#         ("New", "New"),
#         ("Ready", "Ready"),
#         ("In Progress", "In Progress"),
#         ("Done", "Done"),
#     ]

#     subject = models.CharField(max_length=300)
#     description = models.TextField(blank=True)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name="userstories")

#     ref = models.PositiveIntegerField(default=0) 

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default="New"
#     )
#     points = models.CharField(max_length=10, default="?")

#     created_at = models.DateTimeField(auto_now_add=True)

#     sprint = models.ForeignKey(
#         "sprints.Sprint",
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name="userstories"
#     )

#     def __str__(self):
#         return self.subject


from django.db import models
from projects.models import Project


class UserStory(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Ready", "Ready"),
        ("In Progress", "In Progress"),
        ("Done", "Done"),
    ]

    subject = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="userstories"
    )

    sprint = models.ForeignKey(
        "sprints.Sprint",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="userstories"
    )

    ref = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New"
    )
    points = models.CharField(max_length=10, default="?")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ref"]

    def __str__(self):
        return f"#{self.ref} {self.subject}"
