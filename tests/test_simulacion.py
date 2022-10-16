from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_response():
    response = client.get('/simulacion')
    assert response.status_code == 200
