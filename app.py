from flask import Flask, render_template
from models import Task

app = Flask(__name__)


@app.route("/")
def home():
    tasks = [
        Task("Finish Flask", "10 July"),
        Task("Learn SQL", "11 July"),
        Task("Practice LeetCode", "12 July")
    ]

    return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)