def test_correct_login(client, user1):
    response = client.post(
        '/login',
        data={
            "username": "leandro",
            "password": "42787067"
        }
    )
    assert response.status_code == 200


def test_wrong_user_login(client, user1):
    response = client.post(
        '/login',
        data={
            "username": "UsuarioQueNoExiste",
            "password": "contraseñaGenerica123"
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': "User doesn't exist."}


def test_wrong_password_login(client, user1):
    response = client.post(
        '/login',
        data={
            "username": "leandro",
            "password": "contraseñaGenericaNoExistente123"
        }
    )
    assert response.status_code == 401
    assert response.json() == {'detail': "Wrong Password."}
