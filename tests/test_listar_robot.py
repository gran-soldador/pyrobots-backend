def test_empty_robot_list(loggedin_client, user1):
    response = loggedin_client.get('/lista-robots')
    assert response.status_code == 400
    assert response.json() == {'detail': 'No se encontraron robots'}


def test_non_empty_robot_list(loggedin_client, user1, robot1):
    response = loggedin_client.get('/lista-robots')
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'nombre': 'robocop'}]