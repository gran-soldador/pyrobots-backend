def test_empty_robot_list(loggedin_client, user1):
    response = loggedin_client.get('/robot/list')
    assert response.status_code == 400
    assert response.json() == {'detail': 'No se encontraron robots'}


def test_non_empty_robot_list(loggedin_client, user1, robot1):
    response = loggedin_client.get('/robot/list')
    assert response.status_code == 200
    avt = 'http://localhost:9000/robotAvatars/1robocopAvatar.png'
    assert response.json() == [{'id': 1, 'name': 'RandomRobot',
                                'avatar': avt,
                                'played': 0, 'won': 0,
                                'avg_rounds': 0}]
