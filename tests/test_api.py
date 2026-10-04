from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_evaluation_endpoint():

    response = client.get(
        "/evaluation"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    evaluation = data["evaluation"]

    assert evaluation["total_test_queries"] == 4

    assert evaluation["recall_at_3"] == 1.0

    assert evaluation["retrieval_accuracy"] == 1.0


def test_empty_question():

    response = client.post(
        "/ask",
        json={
            "question": ""
        }
    )

    assert response.status_code == 400


def test_ask_endpoint():

    response = client.post(
        "/ask",
        json={
            "question":
                "How does UserManager create a user?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    assert "answer" in data

    assert "sources" in data

    assert "metrics" in data

    assert len(data["sources"]) > 0