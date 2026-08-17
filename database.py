import os
import sqlite3
from contextlib import closing

from models import Task


def get_connection():  

    database_path = os.environ.get(
        "DATABASE_PATH",
        "tasks.db"
    )

    connection = sqlite3.connect(database_path)

    return connection


def create_table():
    with closing(get_connection()) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                deadline TEXT,
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)
        connection.commit()


def add_task(task):
    with closing(get_connection()) as connection:
        connection.execute(
            """
            INSERT INTO tasks (title, deadline, completed)
            VALUES (?, ?, ?)
            """,
            (task.title, task.deadline, task.completed)
        )
        connection.commit()


def get_all_tasks():
    with closing(get_connection()) as connection:
        rows = connection.execute("""
            SELECT id, title, deadline, completed
            FROM tasks
            ORDER BY
                completed ASC,
                CASE WHEN deadline IS NULL OR deadline = '' THEN 1 ELSE 0 END,
                deadline ASC,
                id DESC
        """).fetchall()

    return [_row_to_task(row) for row in rows]


def mark_task_completed(task_id):
    with closing(get_connection()) as connection:
        cursor = connection.execute("""
            UPDATE tasks
            SET completed = 1
            WHERE id = ?
        """, (task_id,))
        task_found = cursor.rowcount > 0
        connection.commit()

    return task_found


def delete_task(task_id):
    with closing(get_connection()) as connection:
        cursor = connection.execute("""
            DELETE FROM tasks
            WHERE id = ?
        """, (task_id,))
        task_found = cursor.rowcount > 0
        connection.commit()

    return task_found


def get_task_by_id(task_id):
    with closing(get_connection()) as connection:
        row = connection.execute("""
            SELECT id, title, deadline, completed
            FROM tasks
            WHERE id = ?
        """, (task_id,)).fetchone()

    if row is None:
        return None

    return _row_to_task(row)


def update_task(task_id, title, deadline):
    with closing(get_connection()) as connection:
        cursor = connection.execute("""
            UPDATE tasks
            SET title = ?, deadline = ?
            WHERE id = ?
        """, (title, deadline, task_id))
        task_found = cursor.rowcount > 0
        connection.commit()

    return task_found


def _row_to_task(row):
    return Task(
        title=row[1],
        deadline=row[2],
        completed=bool(row[3]),
        task_id=row[0]
    )
