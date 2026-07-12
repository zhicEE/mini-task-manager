# Mini Task Manager

A simple task management web application built with Flask and SQLite.

## Tech Stack

- Python
- Flask
- SQLite
- HTML / Jinja2
- Git

## Current Features

- Display tasks from SQLite database
- Create new tasks through HTML forms
- Store tasks in SQLite database
- Use Python class (`Task`) to represent task objects
- Convert database records into Python objects
- Render dynamic HTML templates with Jinja2

## Project Structure

```text
mini-task-manager/
├── app.py              # Flask application and routes
├── models.py           # Task class definition
├── database.py         # SQLite database operations
├── templates/
│   └── index.html      # HTML template
├── requirements.txt
└── README.md
```

## Learning Goals

This project is built to practice:

- Flask routing
- GET and POST requests
- HTML forms
- Jinja2 templates
- Python Object-Oriented Programming
- SQLite database operations
- Backend data flow
- Git version control

## Backend Workflow

```text
User Input
    ↓
Flask Route
    ↓
Task Object
    ↓
SQLite Database
    ↓
Flask Template
    ↓
HTML Page
```

## Future Features

- Mark tasks as completed
- Delete tasks
- Edit tasks
- Improve UI design
- Add user authentication
