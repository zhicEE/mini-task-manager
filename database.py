import sqlite3
from models import Task


def get_connection():
    connection = sqlite3.connect("tasks.db")
    return connection


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            deadline TEXT,
            completed INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def add_task(task):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (
            title, deadline, completed
        )
        VALUES (?, ?, ?)
        """,
        (
            task.title,
            task.deadline,
            task.completed
        )
    )

    connection.commit()
    connection.close()


def get_all_tasks():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    task_objects = []
    
    for row in tasks:
        task = Task(
            row[1],
            row[2],
            bool(row[3]),
            row[0]
        )

        task_objects.append(task)

    connection.close()
    return task_objects


def mark_task_completed(task_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = 1
        WHERE id = ?
    """, (task_id,))

    connection.commit()
    connection.close()


def delete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = ?
    """, (task_id,))

    connection.commit()
    connection.close()


