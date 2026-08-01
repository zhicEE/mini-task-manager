from datetime import date
import re
from flask import Flask, render_template, request, redirect, flash
from database import create_table, get_all_tasks, add_task, mark_task_completed, delete_task, get_task_by_id, update_task
from models import Task

app = Flask(__name__)

app.secret_key = "dev-secret-key"


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

    title = request.form["title"]
    deadline = request.form["deadline"]

    if not title.strip():
        flash("Title cannot be empty!")
        return redirect("/")

    deadline_error = validate_deadline(deadline)

    if deadline_error:
        flash(deadline_error)
        return redirect("/")

    task = Task(title, deadline)
    add_task(task)

    flash("Task added successfully!")

    return redirect("/")

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):

    task_found = mark_task_completed(task_id)

    if not task_found:
        return "Task not found", 404

    flash("Task marked as completed!")

    return redirect("/")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):

    task_found = delete_task(task_id)

    if not task_found:
        return "Task not found", 404

    flash("Task deleted successfully!")

    return redirect("/")

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    if request.method == "POST":
        title = request.form["title"]
        deadline = request.form["deadline"]

        if not title.strip():
            flash("Title cannot be empty!")
            return redirect(f"/edit/{task_id}")

        deadline_error = validate_deadline(deadline)

        if deadline_error:
            flash(deadline_error)
            return redirect(f"/edit/{task_id}")

        update_task(task_id, title, deadline)

        flash("Task updated successfully!")
        return redirect("/")
    
    task = get_task_by_id(task_id)

    if task is None:
        return "Task not found", 404
    
    return render_template("edit.html", task=task)


if __name__ == "__main__":
    create_table()
    app.run(debug=True)