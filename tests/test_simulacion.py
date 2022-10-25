import mock


def test_simulacion_ok(client):
    with mock.patch("engine.run_demo_game", return_value={"x": "y"}):
        response = client.get('/simulacion')
    assert response.status_code == 200
    assert response.json() == {"x": "y"}


def test_simulacion_fail(client):
    with mock.patch("engine.run_demo_game", side_effect=ValueError()):
        response = client.get('/simulacion')
    assert response.status_code == 400
