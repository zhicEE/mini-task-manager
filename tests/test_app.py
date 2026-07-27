import pytest
import sqlite3

from app import app


@pytest.fixture
def client(db_path):

    app.config.update(
        TESTING=True
    )

    return app.test_client()

@pytest.fixture
def db_path(tmp_path, monkeypatch):

    test_database = tmp_path / "test_tasks.db"

    monkeypatch.setenv(
        "DATABASE_PATH",
        str(test_database)
    )

    import database

    database.create_table()

    return test_database


def test_home_page(client):

    response = client.get("/")

    assert response.status_code == 200


def test_create_task(client, db_path):

    response = client.post(
        "/add",
        data={
            "title": "Learn Pytest",
            "deadline": ""
        },
        follow_redirects=True
    )

    tasks = get_tasks(db_path)

    assert response.status_code == 200
    assert b"Learn Pytest" in response.data
    assert len(tasks) == 1


def test_empty_title_not_created(client, db_path):

    response = client.post(
        "/add",
        data={
            "title": "",
            "deadline": ""
        },
        follow_redirects=True
    )

    tasks = get_tasks(db_path)

    assert response.status_code == 200
    assert len(tasks) == 0


def test_edit_task(client, db_path):

    client.post(
        "/add",
        data={
            "title": "Old Title",
            "deadline": ""
        }
    )

    tasks = get_tasks(db_path)

    task_id = tasks[0][0]

    response = client.post(
        f"/edit/{task_id}",
        data={
            "title": "New Title",
            "deadline": ""
        },
        follow_redirects=True
    )

    updated_tasks = get_tasks(db_path)

    assert response.status_code == 200
    assert len(updated_tasks) == 1
    assert updated_tasks[0][1] == "New Title"
    assert b"New Title" in response.data


def test_complete_task(client, db_path):

    client.post(
        "/add",
        data={
            "title": "Test Task",
            "deadline": ""
        }
    )

    tasks = get_tasks(db_path)

    task_id = tasks[0][0]

    response = client.post(
        f"/complete/{task_id}",
        follow_redirects=True
    )

    updated_tasks = get_tasks(db_path)

    assert response.status_code == 200
    assert len(updated_tasks) == 1
    assert updated_tasks[0][3] == 1
    assert b"Test Task" in response.data


def get_tasks(db_path):

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tasks"
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks