from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from taskmanager.models import Team, Project, Task
from datetime import date, timedelta

class Command(BaseCommand):
    help = "Seed the database with sample users, teams, projects, and tasks"

    def handle(self, *args, **kwargs):
        # --- 1. Create Users ---
        users = {
            'admin': CustomUser.objects.create_user(username='admin1', email='admin1@example.com', password='adminpass', role='Admin'),
            'manager': CustomUser.objects.create_user(username='manager1', email='manager1@example.com', password='managerpass', role='Manager'),
            'hr': CustomUser.objects.create_user(username='hr1', email='hr1@example.com', password='hrpass', role='HR'),
            'employee': CustomUser.objects.create_user(username='employee1', email='employee1@example.com', password='employeepass', role='Employee'),
        }
        self.stdout.write(self.style.SUCCESS('✅ Users created'))

        # --- 2. Create Teams ---
        team1 = Team.objects.create(name="Alpha Team")
        team1.members.add(users['manager'], users['employee'])

        team2 = Team.objects.create(name="Beta Team")
        team2.members.add(users['hr'], users['employee'])

        self.stdout.write(self.style.SUCCESS('✅ Teams created'))

        # --- 3. Create Projects ---
        proj1 = Project.objects.create(name="Website Redesign", team=team1)
        proj2 = Project.objects.create(name="Recruitment Drive", team=team2)

        self.stdout.write(self.style.SUCCESS('✅ Projects created'))

        # --- 4. Create Tasks ---
        Task.objects.create(
            title="Design UI",
            description="Create mockups and wireframes",
            assigned_to=users['employee'],
            project=proj1,
            status='in_progress',
            due_date=date.today() + timedelta(days=7)
        )

        Task.objects.create(
            title="Backend API",
            description="Develop REST APIs",
            assigned_to=users['employee'],
            project=proj1,
            status='pending',
            due_date=date.today() + timedelta(days=14)
        )

        Task.objects.create(
            title="Interview Scheduling",
            description="Schedule interviews for candidates",
            assigned_to=users['hr'],
            project=proj2,
            status='pending',
            due_date=date.today() + timedelta(days=5)
        )

        self.stdout.write(self.style.SUCCESS('✅ Tasks created'))
