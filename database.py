import sqlite3


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


def add_task(title, deadline):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, deadline)
        VALUES (?, ?)
    """, (title, deadline))

    connection.commit()
    connection.close()


def get_all_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    connection.close()
    return tasks


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

if __name__ == "__main__":
    create_table()
    add_task("Learn CRUD", "14 July")
    tasks = get_all_tasks()
    print(tasks)