# taskmanager/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Manager Dashboard & Sections
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/projects/', views.manager_projects, name='manager_projects'),
    path('manager/projects/create/', views.create_project, name='create_project'),
    path('manager/tasks/', views.manager_tasks, name='manager_tasks'),
    path('manager/tasks/create/', views.create_task, name='create_task'),
    path('manager/teams/', views.manager_teams, name='manager_teams'),
    path('manager/teams/create/', views.create_team, name='create_team'),
    path('manager/reports/', views.manager_reports, name='manager_reports'),

    # HR Tools
    path('teams/', views.view_teams, name='view_teams'),
    path('employees/', views.manage_employees, name='manage_employees'),

    # Employee Assignment
    path('assign/', views.assign_employee_list, name='assign_employee_list'),
    path('assign/<int:user_id>/', views.assign_employee_to_team, name='assign_employee'),

    # Employee Management
    path('delete-inactive-users/', views.delete_inactive_users, name='delete_inactive_users'),
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete-employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    # Teams (if this is different from manager_teams)
    path('teams/all/', views.team_list, name='team_list'),

    path('employees/add/', views.add_employee, name='add_employee'),



]



urlpatterns += [
    path('export-data/', views.export_data_page, name='export_data_page'),  # Optional view
    path('export-employees/', views.export_employees, name='export_employees'),
]
