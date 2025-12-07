from django.db import models

class UserTypeChoices(models.TextChoices):    
    expert = "expert", "Expert"
    student = "student", "Student"
