from datetime import date
import os
import re
from flask import Flask, flash, redirect, render_template, request, url_for
from database import create_table, get_all_tasks, add_task, mark_task_completed, delete_task, get_task_by_id, update_task
from models import Task

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

# Initialize the database when the application is imported by either the
# development server or a production WSGI server.
create_table()


def validate_deadline(deadline):

    if not deadline:
        return None

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", deadline):
        return "Deadline must be a valid date in YYYY-MM-DD format!"

    try:
        parsed_deadline = date.fromisoformat(deadline)
    except ValueError:
        return "Deadline must be a valid date in YYYY-MM-DD format!"

    if parsed_deadline < date.today():
        return "Deadline cannot be in the past!"

    return None


@app.route("/")
def home():
    tasks = get_all_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    title = (request.form.get("title") or "").strip()
    deadline = (request.form.get("deadline") or "").strip()

    if not title:
        flash("Title cannot be empty!")
        return redirect(url_for("home"))

    deadline_error = validate_deadline(deadline)

    if deadline_error:
        flash(deadline_error)
        return redirect(url_for("home"))

    task = Task(title, deadline)
    add_task(task)

    flash("Task added successfully!")

    return redirect(url_for("home"))

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    task_found = mark_task_completed(task_id)

    if not task_found:
        return "Task not found", 404

    flash("Task marked as completed!")

    return redirect(url_for("home"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    task_found = delete_task(task_id)

    if not task_found:
        return "Task not found", 404

    flash("Task deleted successfully!")

    return redirect(url_for("home"))

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        deadline = (request.form.get("deadline") or "").strip()

        if not title:
            flash("Title cannot be empty!")
            return redirect(url_for("edit", task_id=task_id))

        deadline_error = validate_deadline(deadline)

        if deadline_error:
            flash(deadline_error)
            return redirect(url_for("edit", task_id=task_id))

        task_found = update_task(task_id, title, deadline)

        if not task_found:
            return "Task not found", 404

        flash("Task updated successfully!")

        return redirect(url_for("home"))
    
    task = get_task_by_id(task_id)

    if task is None:
        return "Task not found", 404
    
    return render_template("edit.html", task=task)


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
