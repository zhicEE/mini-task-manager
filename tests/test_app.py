import pytest
import sqlite3

from app import app
from datetime import date, timedelta


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


def test_delete_task(client, db_path):

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
        f"/delete/{task_id}",
        follow_redirects=True
    )

    updated_tasks = get_tasks(db_path)

    assert response.status_code == 200
    assert len(updated_tasks) == 0


def test_save_deadline(client, db_path):

    future_deadline = (
        date.today() + timedelta(days=1)
    ).isoformat()

    response = client.post(
        "/add",
        data={
            "title": "Test Task",
            "deadline": future_deadline
        },
        follow_redirects=True
    )

    tasks = get_tasks(db_path)

    assert response.status_code == 200
    assert len(tasks) == 1
    assert future_deadline.encode() in response.data
    assert tasks[0][2] == future_deadline


def test_edit_nonexistent_task(client, db_path):

    response = client.get("/edit/999")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "deadline",
    [
        "2026/08/01",
        "2026-8-1",
        "not-a-date",
        "2026-02-30",
    ]
)
def test_invalid_deadline_not_created(client, db_path, deadline):

    response=client.post(
        "/add",
        data={"title": "Test Task",
              "deadline": deadline
        },
        follow_redirects=True
    )

    tasks = get_tasks(db_path)

    assert response.status_code == 200
    assert b"Deadline must be a valid date in YYYY-MM-DD format!" in response.data
    assert len(tasks) == 0


@pytest.mark.parametrize(
    ("days_from_today", "expected_task_count"),
    [
        (-1, 0),
        (0, 1),
        (1, 1),
    ]
)
def test_deadline_boundary(
    client,
    db_path,
    days_from_today,
    expected_task_count
):

    deadline = (
        date.today() + timedelta(days=days_from_today)
    ).isoformat()

    response = client.post(
        "/add",
        data={
            "title": "Boundary Test",
            "deadline": deadline
        },
        follow_redirects=True
    )

    tasks = get_tasks(db_path)

    assert response.status_code == 200
    assert len(tasks) == expected_task_count

    if days_from_today < 0:
        assert b"Deadline cannot be in the past!" in response.data


@pytest.mark.parametrize(
    "action",
    [
        "complete",
        "delete",
    ]
)
def test_nonexistent_task_action_returns_404(
    client,
    db_path,
    action
):

    response = client.post(f"/{action}/999")

    tasks = get_tasks(db_path)

    assert response.status_code == 404
    assert b"Task not found" in response.data
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