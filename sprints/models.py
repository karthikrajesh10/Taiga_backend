# # from django.db import models
# # from projects.models import Project


# # class Sprint(models.Model):
# #     name = models.CharField(max_length=200)
# #     project = models.ForeignKey(
# #         Project,
# #         on_delete=models.CASCADE,
# #         related_name="sprints"
# #     )
# #     start_date = models.DateField()
# #     end_date = models.DateField()

# #     is_active = models.BooleanField(default=True)
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     class Meta:
# #         ordering = ["start_date"]

# #     def __str__(self):
# #         return f"{self.project.slug} / {self.name}"

# from django.db import models
# from projects.models import Project

# class Sprint(models.Model):
#     name = models.CharField(max_length=200)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.project.name} - {self.name}"

from django.db import models
from projects.models import Project


class Sprint(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="sprints"
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, db_index=True)

    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.name}"
