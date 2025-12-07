from django.db import models
from account.models import Expert, Student


class CoachingSessionStateChoices(models.TextChoices):
    created = "created", "Created"
    started = "started", "Started"
    completed = "completed", "Completed"


class CoachingSession(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.SET_NULL, null=True, related_name="expert_sessions")
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, related_name="student_sessions")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    state = models.CharField(choices=CoachingSessionStateChoices, default=CoachingSessionStateChoices.created)
