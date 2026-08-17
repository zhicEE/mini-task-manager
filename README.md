# Mini Task Manager

A small task management web application built with Flask, Jinja2, and SQLite. It demonstrates a complete CRUD workflow: create, view, update, complete, and delete tasks from a browser.

## Features

- Add tasks with a title and deadline
- View all saved tasks
- Edit task titles and deadlines
- Mark tasks as completed
- Delete tasks
- Filter tasks by all, active, or completed status
- Prioritize active tasks and sort dated tasks by deadline
- Show task counts and context-aware empty states
- Persist task data in a local SQLite database
- Use a responsive, accessible interface on desktop and mobile
- Validate task input and return clear feedback

## Tech Stack

- Python
- Flask
- SQLite
- Jinja2
- HTML and CSS
- Pytest

## Project Structure

```text
mini-task-manager/
├── app.py              # Flask application and route handlers
├── database.py         # SQLite connection and CRUD operations
├── models.py           # Task model
├── requirements.txt    # Python dependencies
├── pytest.ini          # Test configuration
├── static/
│   └── styles.css      # Responsive interface styles
├── templates/
│   ├── base.html       # Shared page layout
│   ├── edit.html       # Task editing form
│   └── index.html      # Task creation form and task list
├── tests/
│   └── test_app.py     # Application test suite
└── README.md
```

The local `tasks.db` file is generated at runtime and is intentionally excluded from Git.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/zhicEE/mini-task-manager.git
cd mini-task-manager
```

### 2. Create and activate a virtual environment

macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open <http://127.0.0.1:5000> in your browser. The SQLite database and `tasks` table are created automatically the first time the application starts.

To enable Flask's debugger during local development:

```bash
FLASK_DEBUG=1 python app.py
```

The built-in Flask server is intended for local development only.

## Configuration

| Environment variable | Purpose | Default |
| --- | --- | --- |
| `DATABASE_PATH` | Location of the SQLite database | `tasks.db` |
| `SECRET_KEY` | Flask session signing key | Local development value |
| `FLASK_DEBUG` | Enable debug mode when set to `1` | Disabled |

Set a strong `SECRET_KEY` when running the app outside local development.

## Tests

Run the complete test suite with:

```bash
pytest
```

Tests use an isolated temporary SQLite database and cover task creation, editing, completion, deletion, validation, ordering, filtering, and missing-resource behavior.

## Routes

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/` | Display all tasks |
| `POST` | `/add` | Create a task |
| `GET` | `/edit/<task_id>` | Display the edit form |
| `POST` | `/edit/<task_id>` | Save changes to a task |
| `POST` | `/complete/<task_id>` | Mark a task as completed |
| `POST` | `/delete/<task_id>` | Delete a task |

After each form action, the application redirects to the main task list.

## Data Model

Each task contains:

| Field | Description |
| --- | --- |
| `id` | Auto-incrementing SQLite identifier |
| `title` | Task title |
| `deadline` | Deadline stored as text |
| `completed` | Completion status, stored as `0` or `1` |

Database rows are converted into `Task` objects before being rendered by the templates.

## How It Works

```text
Browser form
    ↓
Flask route
    ↓
Task object / database operation
    ↓
SQLite
    ↓
Redirect to the task list
    ↓
Jinja2 renders the updated page
```

`base.html` defines the shared HTML structure and page title block. `index.html` and `edit.html` extend that base template and provide their own page content.

## Learning Goals

This project is designed to practice:

- Flask routing and dynamic URL parameters
- GET and POST requests
- HTML forms and redirects
- Jinja2 loops, conditions, and template inheritance
- Python object-oriented programming
- SQLite CRUD operations
- Converting database records into Python objects
- Input validation and error handling
- Automated testing with isolated data
- Responsive and accessible interface design
- Git version control
