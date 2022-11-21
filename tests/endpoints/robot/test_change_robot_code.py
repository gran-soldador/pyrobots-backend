def test_code_file_not_py(loggedin_client, user1, robot1):
    with open("tests/archivosParaTests/notAnImage.txt", "rb") as c:
        response = loggedin_client.post(
            '/robot/edit_implementation',
            data={"robot_id": robot1},
            files={"new_code": c},
        )
        assert response.status_code == 400
        assert response.json() == {'detail': "File must be a .py"}


def test_invalid_id(loggedin_client, user1, robot1):
    with open("tests/archivosParaTests/codeOfRobot.py", "rb") as c:
        response = loggedin_client.post(
            '/robot/edit_implementation',
            data={"robot_id": 55},
            files={"new_code": c},
        )
        assert response.status_code == 400
        assert response.json() == {'detail': "Invalid robot."}


def test_correct_change_of_code(loggedin_client, user1, robot1):
    with open("tests/archivosParaTests/codeOfRobot.py", "rb") as c:
        response = loggedin_client.post(
            '/robot/edit_implementation',
            data={"robot_id": robot1},
            files={"new_code": c},
        )
        assert response.status_code == 200
        assert response.json() == {'detail': "Robot code succesfully changed."}
