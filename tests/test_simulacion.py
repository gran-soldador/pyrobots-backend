from fastapi.testclient import TestClient
import mock
from main import app

client = TestClient(app)


def test_simulacion_ok():
    with mock.patch("engine.run_demo_game", return_value={"x": "y"}):
        response = client.get('/simulacion')
    assert response.status_code == 200


def test_simulacion_fail():
    with mock.patch("engine.run_demo_game", side_effect=ValueError()):
        response = client.get('/simulacion')
    assert response.status_code == 400
