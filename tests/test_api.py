import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.deps import get_db, get_current_user, get_current_active_admin
from app.models.schema import User

client = TestClient(app)

# Mock user data
mock_user = User(id=1, username="testuser", role="user")
mock_admin = User(id=2, username="adminuser", role="admin")

# Dependency overrides
def override_get_db():
    return MagicMock()

def override_get_current_user():
    return mock_user

def override_get_current_active_admin():
    return mock_admin

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_current_active_admin] = override_get_current_active_admin

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Domain Q&A Copilot API"}

@patch("app.services.generator.generator.generate_answer")
def test_ask_question(mock_gen):
    mock_gen.return_value = {"answer": "This is a test answer", "sources": [{"source": "test.pdf"}]}
    response = client.post("/api/v1/query/", json={"question": "What is this?"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert response.json()["answer"] == "This is a test answer"

@patch("app.db.vector.vector_db.add_documents")
def test_upload_document(mock_add):
    # Mock pypdf and io if needed, but here we just test the endpoint logic
    # Using a simple text file for simplicity in test
    file_content = b"This is some test content"
    files = {"file": ("test.txt", file_content, "text/plain")}
    response = client.post("/api/v1/ingest/upload", files=files)
    assert response.status_code == 200
    assert "Successfully ingested" in response.json()["message"]

def test_submit_feedback():
    response = client.post("/api/v1/feedback/", json={
        "query": "test query",
        "answer": "test answer",
        "score": 1
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Feedback submitted successfully"
