from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib.auth import get_user_model
import csv

from .models import Task, Project, Team
from .forms import TaskForm
from accounts.models import CustomUser

User = get_user_model()

# -------------------------
# 🟦 MANAGER DASHBOARD & NAVIGATION
# -------------------------

@login_required
def manager_dashboard(request):
    return render(request, 'accounts/manager_dashboard.html')

@login_required
def manager_projects(request):
    projects = Project.objects.all()
    return render(request, 'taskmanager/manager_projects.html', {'projects': projects})

@login_required
def manager_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'taskmanager/manager_tasks.html', {'tasks': tasks})

@login_required
def manager_teams(request):
    teams = Team.objects.all()
    return render(request, 'taskmanager/manager_teams.html', {'teams': teams})

@login_required
def manager_reports(request):
    return render(request, 'taskmanager/manager_reports.html')


# -------------------------
# ✅ CREATE PROJECT
# -------------------------

@login_required
def create_project(request):
    teams = Team.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        team_id = request.POST.get('team')
        team = get_object_or_404(Team, id=team_id)
        Project.objects.create(name=name, description=description, team=team)
        return redirect('manager_projects')
    return render(request, 'taskmanager/create_project.html', {'teams': teams})


# -------------------------
# ✅ CREATE TASK
# -------------------------

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('manager_tasks')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'taskmanager/create_task.html', {'form': form})


# -------------------------
# ✅ CREATE TEAM
# -------------------------

@login_required
def create_team(request):
    users = CustomUser.objects.filter(role='employee')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        member_ids = request.POST.getlist('members')
        if name:
            team = Team.objects.create(name=name, description=description)
            team.members.set(member_ids)
            team.save()
            messages.success(request, 'Team created successfully!')
            return redirect('manager_teams')
        else:
            messages.error(request, 'Please provide a team name.')
    return render(request, 'taskmanager/create_team.html', {'users': users})


# -------------------------
# ✅ ASSIGN EMPLOYEE TO TEAM (HR)
# -------------------------

@login_required
def assign_employee_list(request):
    employees = CustomUser.objects.filter(role='employee')
    return render(request, 'taskmanager/assign_employee_list.html', {'employees': employees})

@login_required
def assign_employee_to_team(request, user_id):
    employee = get_object_or_404(CustomUser, id=user_id, role='employee')
    teams = Team.objects.all()
    if request.method == 'POST':
        team_id = request.POST.get('team')
        if team_id:
            team = get_object_or_404(Team, id=team_id)
            employee.team = team
            employee.save()
            team.members.add(employee)
            messages.success(request, f"{employee.username} assigned to {team.name}.")
            return redirect('assign_employee_list')
    return render(request, 'taskmanager/assign_form.html', {'employee': employee, 'teams': teams})


# -------------------------
# ✅ VIEW TEAMS
# -------------------------

@login_required
def view_teams(request):
    teams = Team.objects.all()
    return render(request, 'taskmanager/view_teams.html', {'teams': teams})


# -------------------------
# ✅ EXPORT EMPLOYEES (HR/Admin)
# -------------------------

@login_required
def export_employees(request):
    if request.user.role.lower() not in ['hr', 'admin']:
        return HttpResponse("Unauthorized", status=401)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Role'])

    employees = CustomUser.objects.filter(role='employee')
    for emp in employees:
        writer.writerow([emp.username, emp.email, emp.role])

    return response


# -------------------------
# ✅ EXPORT DATA PAGE
# -------------------------

def is_hr(user):
    return user.is_authenticated and user.role.lower() == 'hr'

def export_data_page(request):
    return render(request, 'taskmanager/export_data.html')


# -------------------------
# ✅ DELETE INACTIVE USERS (HR)
# -------------------------

@login_required
@user_passes_test(lambda u: u.role.lower() == 'hr')
def delete_inactive_users(request):
    inactive_users = CustomUser.objects.filter(is_active=False)
    count = inactive_users.count()
    inactive_users.delete()
    messages.success(request, f'{count} inactive users deleted successfully.')
    return redirect('hr_dashboard')


# -------------------------
# ✅ EDIT EMPLOYEE (HR)
# -------------------------

@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(CustomUser, id=employee_id)
    if request.method == 'POST':
        employee.username = request.POST.get('username')
        employee.email = request.POST.get('email')
        employee.save()
        messages.success(request, 'Employee updated successfully.')
        return redirect('hr_dashboard')
    return render(request, 'taskmanager/edit_employee.html', {'employee': employee})


# -------------------------
# ✅ DELETE EMPLOYEE (HR)
# -------------------------

@login_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(CustomUser, id=employee_id, role='employee')
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully.')
        return redirect('hr_dashboard')
    return render(request, 'taskmanager/confirm_delete.html', {'employee': employee})


# -------------------------
# ✅ MANAGE EMPLOYEES (HR)
# -------------------------

@login_required
def manage_employees(request):
    employees = User.objects.filter(role='employee')
    return render(request, 'taskmanager/manage_employees.html', {'employees': employees})


# -------------------------
# ✅ TEAM LIST
# -------------------------

@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'taskmanager/team_list.html', {'teams': teams})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import CustomUser
from django.contrib import messages

# ✅ Restrict to HR users only
def is_hr(user):
    return user.is_authenticated and user.role == 'HR'

# ✅ View to add an employee
def add_employee(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')  # You can fix this as 'Employee' if needed

        # ✅ Validation
        if not all([username, email, password, role]):
            messages.error(request, "All fields are required.")
            return redirect('add_employee')

        # ✅ Create user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        messages.success(request, f"Employee '{username}' added successfully!")
        return redirect('manage_employees')  # Or any HR dashboard page

    return render(request, 'taskmanager/add_employee.html')  # Make sure this template exists
