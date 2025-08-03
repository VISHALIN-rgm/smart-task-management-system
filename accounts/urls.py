from django.urls import path
from . import views

urlpatterns = [
    # ======= Registration URLs =======
    path('register/admin/', views.register_admin, name='register_admin'),
    path('register/manager/', views.register_manager, name='register_manager'),
    path('register/hr/', views.register_hr, name='register_hr'),
    path('register/employee/', views.register_employee, name='register_employee'),

    # ======= Login URLs =======
    path('login/admin/', views.login_admin, name='login_admin'),
    path('login/manager/', views.login_manager, name='login_manager'),
    path('login/hr/', views.login_hr, name='login_hr'),
    path('login/employee/', views.login_employee, name='login_employee'),

    # ======= Dashboard URLs =======
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/manager/', views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/hr/', views.hr_dashboard, name='hr_dashboard'),
    path('dashboard/employee/', views.employee_dashboard, name='employee_dashboard'),

    # ======= Admin Panel Features =======
    path('dashboard/admin/add-manager/', views.add_manager, name='add_manager'),
    path('dashboard/admin/add-hr/', views.add_hr, name='add_hr'),
    path('dashboard/admin/users/', views.admin_users, name='admin_users'),
    path('dashboard/admin/teams/', views.admin_teams, name='admin_teams'),
    path('dashboard/admin/projects/', views.admin_projects, name='admin_projects'),
    path('dashboard/admin/reports/', views.admin_reports, name='admin_reports'),

    # ======= Export Users =======
    path('dashboard/admin/export-users/', views.export_users_view, name='export_users_view'),
    path('dashboard/admin/export-users/csv/', views.export_users_csv, name='export_users_csv'),

    # ======= Logout =======
    path('logout/', views.logout_user, name='logout'),
]
