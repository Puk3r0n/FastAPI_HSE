from fastapi.testclient import TestClient
from gg import app

client = TestClient(app)


def test_create_task():
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description", "status": "in_progress"})
    assert response.status_code == 422
    assert response.json()["title"] == "Test Task"
    assert response.json()["description"] == "Test Description"
    assert response.json()["status"] == "in_progress"


def test_get_task_by_id():
    response = client.get("/tasks/0")
    assert response.status_code == 404
    assert response.json()["task_id"] == 0


def test_update_task():
    response = client.put("/tasks/0", json={"title": "Updated Task",
                                            "description": "Updated Description",
                                            "status": "completed"})
    assert response.status_code == 422
    assert response.json()["title"] == "Updated Task"
    assert response.json()["description"] == "Updated Description"
    assert response.json()["status"] == "completed"


def test_get_tasks_by_status():
    response = client.get("/tasks/by_status?status=in_progress")
    assert response.status_code == 422
    assert len(response.json()) > 0


def test_read_tasks():
    response = client.get("/tasks?sort_by=title&search_text=Test")
    assert response.status_code == 405
    assert len(response.json()) > 0


def test_delete_task():
    response = client.delete("/tasks/0")
    assert response.status_code == 404
    assert response.json()["task_id"] == 0


def test_get_priority_tasks():
    response = client.get("/tasks/priority/?top_n=5")
    assert response.status_code == 404
    assert len(response.json()) <= 5
