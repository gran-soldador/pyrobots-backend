from fastapi.testclient import TestClient
from main import app
from db import *
from endpoints.functions_jwt import authenticated_user
import pytest

_client = TestClient(app)


@pytest.fixture()
def client():
    return _client


@pytest.fixture()
def mocked_login():
    app.dependency_overrides = {authenticated_user: lambda: 1}
    yield
    app.dependency_overrides = {}
    return


@pytest.fixture()
def loggedin_client(client, mocked_login):
    return client


@pytest.fixture(autouse=True)
def reset_db():
    db.drop_all_tables(True)
    db.create_tables()


@pytest.fixture
@db_session
def user1():
    user = Usuario(nombre_usuario='leandro',
                   email='leandro.lopez@mi.unc.edu.ar',
                   contraseña='42787067', verificado=True)
    user.flush()
    return user.user_id


@pytest.fixture
@db_session
def user2():
    user = Usuario(nombre_usuario='luigi',
                   email='luigifinetti@mi.unc.edu.ar',
                   contraseña='1234ABCDa!', verificado=True)
    user.flush()
    return user.user_id


@pytest.fixture
@db_session
def robot1(user1):
    robot = Robot(nombre='robocop', implementacion='super-robot.py',
                  partidas_ganadas=0, partidas_jugadas=0,
                  defectuoso=False, usuario=Usuario[user1])
    robot.flush()
    return robot.robot_id
