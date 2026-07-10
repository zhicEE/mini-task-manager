from flask import Flask, render_template
from database import create_table, get_all_tasks

app = Flask(__name__)


@app.route("/")
def home():
    tasks = get_all_tasks()
    return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    create_table()
    app.run(debug=True)