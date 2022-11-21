def test_view_profile(loggedin_client, user1):
    response = loggedin_client.get('/user/profile')
    assert response.status_code == 200
    assert response.json() == {
        'username': 'leandro',
        'mail': 'leandro.lopez@mi.unc.edu.ar',
        'avatar': 'http://localhost:9000/avatars/leandroUserAvatar.png'
    }
