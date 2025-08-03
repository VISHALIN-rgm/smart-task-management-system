from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # This avoids circular import

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_teams',
        limit_choices_to={'role': 'manager'}
    )

    members = models.ManyToManyField(
        User,
        related_name='teams',
        limit_choices_to={'role': 'employee'}
    )

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20)
    due_date = models.DateField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
