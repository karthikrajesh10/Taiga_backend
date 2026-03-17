from django.db import models
from django.conf import settings
from projects.models import Project
from sprints.models import Sprint
from tasks.models import Task


class TimeLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="time_logs"
    )

    # All nullable — supports non-project learning/personal time logging
    project = models.ForeignKey(
        Project,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="time_logs"
    )
    sprint = models.ForeignKey(
        Sprint,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="time_logs"
    )
    task = models.ForeignKey(
        Task,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="time_logs"
    )

    date = models.DateField()
    worked_hours = models.FloatField()
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["task"]),
            models.Index(fields=["project"]),
            models.Index(fields=["date"]),
        ]
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.user.username} | {self.date} | {self.worked_hours}h"