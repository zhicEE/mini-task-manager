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


def get_tasks(db_path):

    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM tasks"
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks
