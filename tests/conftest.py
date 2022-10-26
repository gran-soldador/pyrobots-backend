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
def mocked_login2():
    app.dependency_overrides = {authenticated_user: lambda: 2}
    yield
    app.dependency_overrides = {}
    return


@pytest.fixture()
def loggedin_client(client, mocked_login):
    return client


@pytest.fixture()
def loggedin_client2(client, mocked_login2):
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


@pytest.fixture
@db_session
def robot2(user2):
    robot = Robot(nombre='robocop', implementacion='super-robot.py',
                  partidas_ganadas=0, partidas_jugadas=0,
                  defectuoso=False, usuario=Usuario[user2])
    robot.flush()
    return robot.robot_id


@pytest.fixture
@db_session
def robot3(user1):
    robot = Robot(nombre='robot', implementacion='super-robot.py',
                  partidas_ganadas=0, partidas_jugadas=0,
                  defectuoso=False, usuario=Usuario[user1])
    robot.flush()
    return robot.robot_id


@pytest.fixture
@db_session
def partida1(robot1, user1):
    p1 = Partida(namepartida='my_partida', status='disponible',
                 minplayers=3, maxplayers=3, numgames=10, numrondas=10,
                 creador=Usuario[user1])
    p1.participante.add(Robot[robot1])
    p1.flush()
    return p1.partida_id


@pytest.fixture
@db_session
def partida2(robot1, user1):
    p2 = Partida(namepartida='my_partida', password='leandro',
                 status='disponible',
                 minplayers=3, maxplayers=3, numgames=10, numrondas=10,
                 creador=Usuario[user1])
    p2.participante.add(Robot[robot1])
    p2.flush()
    return p2.partida_id


@pytest.fixture
@db_session
def partida3(user1):
    p3 = Partida(namepartida='my_partida', password='leandro',
                 status='ocupada',
                 minplayers=3, maxplayers=3, numgames=10, numrondas=10,
                 creador=Usuario[user1])
    p3.flush()
    return p3.partida_id


@pytest.fixture
@db_session
def partida4(user1, robot2):
    p4 = Partida(namepartida='my_partida', password='leandro',
                 status='disponible',
                 minplayers=3, maxplayers=3, numgames=10, numrondas=10,
                 creador=Usuario[user1])
    p4.participante.add(Robot[robot2])
    p4.flush()
    return p4.partida_id


@pytest.fixture
@db_session
def partida5(user1, robot1, robot3):
    p5 = Partida(namepartida='my_partida', password='leandro',
                 status='disponible',
                 minplayers=2, maxplayers=3, numgames=10, numrondas=10,
                 creador=Usuario[user1])
    p5.participante.add(Robot[robot1])
    p5.participante.add(Robot[robot3])
    p5.flush()
    return p5.partida_id


@pytest.fixture
@db_session
def partida6(user1, robot2):
    p5 = Partida(namepartida='my_partida', password='leandro',
                 status='iniciada',
                 minplayers=2, maxplayers=3, numgames=10, numrondas=10,
                 creador=Usuario[user1])
    p5.participante.add(Robot[robot2])
    p5.flush()
    return p5.partida_id
