from flask import Flask, render_template, request, redirect
from database import create_table, get_all_tasks, add_task, mark_task_completed
from models import Task

app = Flask(__name__)


@app.route("/")
def home():

    tasks = get_all_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():

    title = request.form["title"]
    deadline = request.form["deadline"]

    task = Task(title, deadline)
    add_task(task)

    return redirect("/")

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    mark_task_completed(task_id)
    return redirect("/")

if __name__ == "__main__":
    create_table()
    app.run(debug=True)