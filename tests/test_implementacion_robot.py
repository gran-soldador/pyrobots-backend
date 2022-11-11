def test_correct_robot(loggedin_client, robot1):
    response = loggedin_client.get(f'/robot/code/{robot1}')
    assert response.status_code == 200
    assert 'class RandomRobot(Robot):' in response.json()['code']


def test_non_exist_robot(loggedin_client):
    response = loggedin_client.get('/robot/code/1')
    assert response.status_code == 400
    assert response.json() == {'detail': 'El robot no existe'}


def test_non_user_robot(loggedin_client2, robot1):
    response = loggedin_client2.get(f'/robot/code/{robot1}')
    assert response.status_code == 400
    assert response.json() == {'detail': 'El robot no pertenece al usuario'}
