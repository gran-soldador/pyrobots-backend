def test_not_image(loggedin_client, user1):
    with open("tests/archivosParaTests/notAnImage.txt", "rb") as c:
        response = loggedin_client.post(
            '/user/profile/change_avatar',
            files={"new_profile": c},
        )
        assert response.status_code == 400
        assert response.json() == {'detail': "File is not an image."}


def test_is_an_image(loggedin_client, user1):
    with open("tests/archivosParaTests/DefaultAvatar.png", "rb") as c:
        response = loggedin_client.post(
            '/user/profile/change_avatar',
            files={"new_profile": c},
        )
        assert response.status_code == 200
        assert response.json() == {'detail': "Profile " +
                                   "picture succesfully changed."}
