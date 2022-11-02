import mock
from dataclasses import asdict

from engine.outputmodels import SimulationResult


def test_simulacion_ok(client):
    res = SimulationResult(rounds_played=10, players=[], winners=[],
                           maxrounds=10, rounds=[])
    with mock.patch("engine.run_demo_game", return_value=res):
        response = client.get('/simulacion')
    assert response.status_code == 200
    assert response.json() == asdict(res)


def test_simulacion_fail(client):
    with mock.patch("engine.run_demo_game", side_effect=ValueError()):
        response = client.get('/simulacion')
    assert response.status_code == 500
