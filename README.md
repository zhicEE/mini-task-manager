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

Then open <http://127.0.0.1:5000> in your browser. The SQLite database is
created automatically when the application starts.

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
