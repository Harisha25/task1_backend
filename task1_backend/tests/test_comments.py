import pytest
from app import create_app, db
from app.models import Task, Comment

@pytest.fixture
def client():
    app = create_app("testing")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app.test_client()

        db.session.remove()
        db.drop_all()

@pytest.fixture
def task():
    t = Task(title="Sample Task")
    db.session.add(t)
    db.session.commit()
    return t

def test_create_comment(client, task):
    response = client.post(f"/api/tasks/{task.id}/comments",
                           json={"content": "hello", "author_name": "John"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["content"] == "hello"

def test_list_comments(client, task):
    c = Comment(task_id=task.id, content="sample")
    db.session.add(c)
    db.session.commit()

    response = client.get(f"/api/tasks/{task.id}/comments")
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_update_comment(client, task):
    c = Comment(task_id=task.id, content="old")
    db.session.add(c)
    db.session.commit()

    response = client.put(
        f"/api/tasks/{task.id}/comments/{c.id}",
        json={"content": "new"}
    )
    assert response.status_code == 200
    assert response.get_json()["content"] == "new"

def test_delete_comment(client, task):
    c = Comment(task_id=task.id, content="to delete")
    db.session.add(c)
    db.session.commit()

    response = client.delete(
        f"/api/tasks/{task.id}/comments/{c.id}"
    )
    assert response.status_code == 204
