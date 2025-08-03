from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.db.models import Count
import csv
from .models import CustomUser  

from .forms import (
    AdminRegisterForm, ManagerRegisterForm, HRRegisterForm,
    EmployeeRegisterForm, ManagerRegistrationForm
)
from taskmanager.models import Team, Project, Task

# ===== Helper Functions =====
def is_admin(user):
    return user.is_authenticated and user.role.lower() == 'admin'

# ========== Registration Views ==========
def register_admin(request):
    form = AdminRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login_admin')
    return render(request, 'accounts/register_admin.html', {'form': form})

def register_manager(request):
    form = ManagerRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login_manager')
    return render(request, 'accounts/register_manager.html', {'form': form})

def register_hr(request):
    form = HRRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login_hr')
    return render(request, 'accounts/register_hr.html', {'form': form})

def register_employee(request):
    form = EmployeeRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login_employee')
    return render(request, 'accounts/register_employee.html', {'form': form})

# ========== Login Views ==========
def login_admin(request):
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.role.lower() == 'admin':
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, "Invalid admin credentials.")
    return render(request, 'accounts/login_admin.html')

def login_manager(request):
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.role.lower() == 'manager':
            login(request, user)
            return redirect('manager_dashboard')
        messages.error(request, "Invalid manager credentials.")
    return render(request, 'accounts/login_manager.html')

def login_hr(request):
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.role.lower() == 'hr':
            login(request, user)
            return redirect('hr_dashboard')
        messages.error(request, "Invalid HR credentials.")
    return render(request, 'accounts/login_hr.html')

def login_employee(request):
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.role.lower() == 'employee':
            login(request, user)
            return redirect('employee_dashboard')
        messages.error(request, "Invalid employee credentials.")
    return render(request, 'accounts/login_employee.html')

# ========== Logout ==========
def logout_user(request):
    logout(request)
    return redirect('login_admin')

# ========== Dashboard Views ==========
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    role_counts = {
        'Admin': CustomUser.objects.filter(role__iexact='admin').count(),
        'HR': CustomUser.objects.filter(role__iexact='hr').count(),
        'Manager': CustomUser.objects.filter(role__iexact='manager').count(),
        'Employee': CustomUser.objects.filter(role__iexact='employee').count(),
    }
    recent_users = CustomUser.objects.all().order_by('-date_joined')[:5]
    all_users = CustomUser.objects.all().order_by('-date_joined')[:50]
    return render(request, 'accounts/admin_dashboard.html', {
        'role_counts': role_counts,
        'recent_users': recent_users,
        'all_users': all_users
    })

@login_required
def manager_dashboard(request):
    employee_count = CustomUser.objects.filter(role='employee').count()
    team_count = Team.objects.count()
    project_count = Project.objects.count()
    
    return render(request, 'accounts/manager_dashboard.html', {
        'employee_count': employee_count,
        'team_count': team_count,
        'project_count': project_count,
    })

from django.shortcuts import render
from accounts.models import CustomUser

def hr_dashboard(request):
    employees = CustomUser.objects.filter(role='employee').select_related('team')  # ✅ no more error
    return render(request, 'accounts/hr_dashboard.html', {'employees': employees})

@login_required
def employee_dashboard(request):
    user = request.user
    tasks = Task.objects.filter(assigned_to=user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    pending_tasks = total_tasks - completed_tasks
    team = Team.objects.filter(members=user).first()
    team_name = team.name if team else "Not Assigned"
    manager = CustomUser.objects.filter(teams=team, role='manager').exclude(id=user.id).first() if team else None
    manager_name = manager.username if manager else "N/A"
    team_members = team.members.exclude(id=user.id).values_list('username', flat=True) if team else []
    return render(request, 'accounts/employee_dashboard.html', {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'team_name': team_name,
        'manager_name': manager_name,
        'team_members': team_members,
    })

# ========== Admin Manage Users, Teams, Projects ==========
@login_required
@user_passes_test(is_admin)
def add_manager(request):
    form = ManagerRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'accounts/add_manager.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def add_hr(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profession = request.POST.get('profession')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            CustomUser.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                role='HR',
                profession=profession
            )
            messages.success(request, "HR user created successfully.")
            return redirect('add_hr')
    hrs = CustomUser.objects.filter(role='HR')
    return render(request, 'accounts/admin_add_hr.html', {'hrs': hrs})

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    all_users = CustomUser.objects.all()
    return render(request, 'accounts/admin_users.html', {'all_users': all_users})

@login_required
@user_passes_test(is_admin)
def admin_teams(request):
    all_teams = Team.objects.all()
    return render(request, 'accounts/admin_teams.html', {'all_teams': all_teams})

@login_required
@user_passes_test(is_admin)
def admin_projects(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        team_id = request.POST.get('team')
        team = Team.objects.get(id=team_id)
        Project.objects.create(name=name, description=description, team=team)
        return redirect('admin_projects')
    projects = Project.objects.select_related('team').all().order_by('-id')
    teams = Team.objects.all()
    return render(request, 'accounts/admin_projects.html', {
        'projects': projects,
        'teams': teams,
    })

@login_required
@user_passes_test(is_admin)
def admin_reports(request):
    role_counts = CustomUser.objects.values('role').annotate(total=Count('id'))
    teams = Team.objects.annotate(member_count=Count('members'))
    total_projects = Project.objects.count()
    projects_per_team = Project.objects.values('team__name').annotate(total=Count('id'))
    task_status = Task.objects.values('status').annotate(total=Count('id'))
    return render(request, 'accounts/admin_reports.html', {
        'role_counts': role_counts,
        'teams': teams,
        'total_projects': total_projects,
        'projects_per_team': projects_per_team,
        'task_status': task_status,
    })

# ========== Export Users ==========
@login_required
@user_passes_test(is_admin)
def export_users_view(request):
    users = CustomUser.objects.all()
    return render(request, 'accounts/export_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Role', 'Date Joined'])
    for user in CustomUser.objects.all():
        writer.writerow([user.username, user.email, user.role, user.date_joined])
    return response
