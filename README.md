# Smart Task Management System (STMS)

> A role-based task management web application built with Django, MySQL, and Chart.js — designed for real teams with Admin, Manager, HR, and Employee workflows.

---

## Overview

STMS is a full-stack web application that streamlines task tracking, team management, and project assignment across an organisation. Each role gets a dedicated dashboard with relevant data, controls, and analytics — no single view for everyone.

Built with a clean Django backend, MySQL database, and Bootstrap frontend with interactive Chart.js dashboards.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| Frontend | HTML5, CSS3, Bootstrap, JavaScript |
| Charts | Chart.js |
| Database | MySQL |
| Auth | Django built-in authentication |

---

## Roles & Access

| Role | Capabilities |
|---|---|
| **Admin** | Full system control — manage all users, roles, teams, projects, and tasks |
| **Manager** | Create and assign tasks, manage team members, track project progress |
| **HR** | Manage employee records, handle registrations, view team structures |
| **Employee** | View assigned tasks, update task status, access personal dashboard |

---

## Features

- **Role-based login & registration** — each role has a dedicated login flow and is redirected to its own dashboard on sign-in
- **Task management** — create, assign, update, and track tasks with status labels (Pending / In Progress / Completed)
- **Team management** — create teams, assign members, and manage team structure
- **Project assignment** — link tasks and teams to specific projects
- **Dashboard charts** — interactive Chart.js visualisations for task status, team performance, and project progress
- **MySQL integration** — relational database with structured schema for users, roles, tasks, teams, and projects

---

## Project Structure

```
smart-task-management-system/
├── accounts/          # User auth, registration, role management
├── tasks/             # Task creation, assignment, status tracking
├── teams/             # Team and member management
├── projects/          # Project management and assignment
├── dashboard/         # Role-specific dashboard views and Chart.js data
├── templates/         # HTML templates per role
├── static/            # CSS, JS, Bootstrap, Chart.js
├── manage.py
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- MySQL 8.0+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/VISHALIN-rgm/smart-task-management-system.git
cd smart-task-management-system

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure the database
# Create a MySQL database and update settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stms_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create a superuser (Admin)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Dashboards

Each role lands on a dedicated dashboard after login:

**Admin Dashboard**
- Overview of all users, teams, and projects
- System-wide task completion chart
- User management controls

**Manager Dashboard**
- Team task status chart (Chart.js)
- Assigned project overview
- Quick task creation and assignment

**HR Dashboard**
- Employee list and profile management
- Registration approvals
- Team structure view

**Employee Dashboard**
- Personal task list with status updates
- Assigned project details
- Progress tracking chart

---

## Database Schema (Key Tables)

```
User         — id, username, email, password, role
Task         — id, title, description, assigned_to, project, status, due_date
Team         — id, name, manager, members (M2M)
Project      — id, name, description, team, start_date, end_date
```


