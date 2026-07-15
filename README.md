# Mini Task Manager

A simple task management web application built with Flask and SQLite.

## Tech Stack

- Python
- Flask
- SQLite
- HTML / Jinja2
- Git

## Current Features

- Display tasks stored in SQLite
- Add new tasks through an HTML form
- Set a deadline for each task
- Mark tasks as completed
- Delete tasks
- Store task data in a local SQLite database
- Represent database records as Python `Task` objects
- Render dynamic pages with Jinja2
- Redirect users back to the task list after form actions

## Project Structure

```text
├── .gitignore
├── app.py              # Flask application and routes
├── database.py         # SQLite database operations
├── models.py           # Task class definition
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # HTML template
└── README.md
```

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/zhicEE/mini-task-manager.git
   cd mini-task-manager
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Flask development server:

```bash
python app.py
```

Then open <http://127.0.0.1:5000> in your browser.

The SQLite database is created automatically when the application starts.

## Backend Workflow

### Adding a Task

```text
User submits HTML form
        ↓
POST /add
        ↓
Flask reads request.form
        ↓
Create a Task object
        ↓
Insert task into SQLite
        ↓
Redirect to /
        ↓
Read tasks from SQLite
        ↓
Render the HTML page
```

### Completing or Deleting a Task

```text
User clicks a button
        ↓
Task ID is added to the URL
        ↓
POST /complete/<task_id>
or
POST /delete/<task_id>
        ↓
Flask receives task_id
        ↓
Update or delete the SQLite record
        ↓
Redirect to /
        ↓
Render the updated task list
```

## Learning Goals

This project is built to practice:

- Flask routing
- GET and POST requests
- HTML forms
- Dynamic URL parameters
- Redirects
- Jinja2 templates
- Python Object-Oriented Programming
- SQLite CRUD operations
- Converting database records into Python objects
- Backend request and response flow
- Git version control

## Future Features

- Edit existing tasks
- Filter tasks by completion status
- Improve form validation
- Improve the user interface
- Add automated tests
- Deploy the application