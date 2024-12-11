import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_empty_todos(client):
    """Test retrieving todos when the list is empty."""
    rv = client.get("/todos")
    assert rv.status_code == 200
    assert rv.get_json() == []


def test_create_todo(client):
    """Test creating a new todo."""
    rv = client.post("/todos", json={"title": "Buy milk"})
    assert rv.status_code == 201
    json_data = rv.get_json()
    assert json_data["title"] == "Buy milk"
    assert json_data["completed"] is False


def test_get_todos(client):
    """Test retrieving todos when the list is not empty."""
    rv = client.get("/todos")
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data[0]["title"] == "Buy milk"


def test_get_todo_by_id(client):
    """Test retrieving a todo by its ID."""
    client.post("/todos", json={"title": "Buy milk"})
    rv = client.get("/todos/1")
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data["title"] == "Buy milk"


def test_get_todo_not_found(client):
    """Test retrieving a non-existent todo."""
    rv = client.get("/todos/999")
    assert rv.status_code == 404
    json_data = rv.get_json()
    assert json_data["error"] == "Todo not found"


def test_update_todo(client):
    """Test updating a todo."""
    client.post("/todos", json={"title": "Buy milk"})
    rv = client.put("/todos/1", json={"title": "Buy bread", "completed": True})
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data["title"] == "Buy bread"
    assert json_data["completed"] is True


def test_update_todo_not_found(client):
    """Test updating a non-existent todo."""
    rv = client.put("/todos/999", json={"title": "Buy bread", "completed": True})
    assert rv.status_code == 404
    json_data = rv.get_json()
    assert json_data["error"] == "Todo not found"


def test_delete_todo(client):
    """Test deleting a todo."""
    client.post("/todos", json={"title": "Buy milk"})
    rv = client.delete("/todos/1")
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data["message"] == "Todo deleted"
    rv = client.get("/todos/1")
    assert rv.status_code == 404


def test_create_todo_missing_title(client):
    """Test creating a new todo without a title."""
    rv = client.post("/todos", json={})
    assert rv.status_code == 400
    json_data = rv.get_json()
    assert json_data["error"] == "Title is required"

