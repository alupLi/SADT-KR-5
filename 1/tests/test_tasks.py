import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import storage

@pytest.fixture
def client():
    storage.clear()
    return TestClient(app)

def test_create_task_success(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Test task",
            "description": "Test description",
            "status": "todo",
            "priority": 3
        },
        headers={"X-User-Id": "10"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["owner_id"] == 10
    assert "id" in data

def test_create_task_title_too_short(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "ab",
            "status": "todo",
            "priority": 3
        },
        headers={"X-User-Id": "10"}
    )
    assert response.status_code == 422

def test_create_task_no_user_id(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Test task",
            "status": "todo",
            "priority": 3
        }
    )
    assert response.status_code == 401

def test_user_sees_only_own_tasks(client):
    # User 10 creates task
    client.post("/tasks/", json={"title": "User10 task", "status": "todo", "priority": 3}, headers={"X-User-Id": "10"})
    # User 20 creates task
    client.post("/tasks/", json={"title": "User20 task", "status": "todo", "priority": 3}, headers={"X-User-Id": "20"})
    
    response = client.get("/tasks/", headers={"X-User-Id": "10"})
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "User10 task"

def test_filter_by_status_and_priority(client):
    client.post("/tasks/", json={"title": "Low priority todo", "status": "todo", "priority": 2}, headers={"X-User-Id": "10"})
    client.post("/tasks/", json={"title": "High priority todo", "status": "todo", "priority": 5}, headers={"X-User-Id": "10"})
    client.post("/tasks/", json={"title": "Done task", "status": "done", "priority": 4}, headers={"X-User-Id": "10"})
    
    response = client.get("/tasks/?status=todo&min_priority=3", headers={"X-User-Id": "10"})
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "High priority todo"

def test_update_task_status_success(client):
    create_resp = client.post("/tasks/", json={"title": "Task", "status": "todo", "priority": 3}, headers={"X-User-Id": "10"})
    task_id = create_resp.json()["id"]
    
    update_resp = client.patch(f"/tasks/{task_id}/status", json={"status": "done"}, headers={"X-User-Id": "10"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "done"

def test_get_foreign_task_returns_404(client):
    client.post("/tasks/", json={"title": "User10 task", "status": "todo", "priority": 3}, headers={"X-User-Id": "10"})
    response = client.get("/tasks/1", headers={"X-User-Id": "20"})
    assert response.status_code == 404

def test_get_nonexistent_task_returns_404(client):
    response = client.get("/tasks/999", headers={"X-User-Id": "10"})
    assert response.status_code == 404

def test_delete_task_success(client):
    create_resp = client.post("/tasks/", json={"title": "To delete", "status": "todo", "priority": 3}, headers={"X-User-Id": "10"})
    task_id = create_resp.json()["id"]
    
    delete_resp = client.delete(f"/tasks/{task_id}", headers={"X-User-Id": "10"})
    assert delete_resp.status_code == 204
    
    get_resp = client.get(f"/tasks/{task_id}", headers={"X-User-Id": "10"})
    assert get_resp.status_code == 404