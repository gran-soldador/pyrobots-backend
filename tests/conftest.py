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
    user = User(name='leandro',
                email='leandro.lopez@mi.unc.edu.ar',
                password='42787067',
                avatar='avatars/leandroUserAvatar.png',
                verified=True)
    user.flush()
    return user.id


@pytest.fixture
@db_session
def user2():
    user = User(name='luigi',
                email='luigifinetti@mi.unc.edu.ar',
                password='1234ABCDa!', verified=True)
    user.flush()
    return user.id


@pytest.fixture
@db_session
def user3():
    user = User(name='rocio',
                email='rocio.cordoba@mi.unc.edu.ar',
                password='asdASD123$', verified=False)
    user.flush()
    return user.id


@pytest.fixture
@db_session
def user4():
    user = User(name='GranSoldador',
                email='test_gran_soldador@hotmail.com',
                password='asdASD123$', verified=True)
    user.flush()
    return user.user_id


@pytest.fixture
@db_session
def robot1(user1):
    with open("tests/archivosParaTests/RandomRobot.py") as f:
        robot = Robot(name='RandomRobot', code=f.read(),
                      avatar='robotAvatars/1robocopAvatar.png',
                      matches_num_won=0, matches_num_played=0,
                      games_won=0, rounds_won=0,
                      defective=False, user=User[user1])
    robot.flush()
    return robot.id


@pytest.fixture
@db_session
def robot2(user2):
    with open("tests/archivosParaTests/GuardRobot.py") as f:
        robot = Robot(name='GuardRobot', code=f.read(),
                      matches_num_won=0, matches_num_played=0,
                      games_won=0, rounds_won=0,
                      defective=False, user=User[user2])
    robot.flush()
    return robot.id


@pytest.fixture
@db_session
def robot3(user1):
    with open("tests/archivosParaTests/SpiralRobot.py") as f:
        robot = Robot(name='SpiralRobot', code=f.read(),
                      matches_num_won=0, matches_num_played=0,
                      games_won=0, rounds_won=0,
                      defective=False, user=User[user1])
    robot.flush()
    return robot.id


@pytest.fixture
@db_session
def robot4(user1):
    with open("tests/archivosParaTests/GuardRobot.py") as f:
        robot = Robot(name='GuardRobot', code=f.read(),
                      matches_num_won=0, matches_num_played=0,
                      games_won=0, rounds_won=0,
                      defective=False, user=User[user1])
    robot.flush()
    return robot.id


@pytest.fixture
@db_session
def partida1(robot1, user1):
    p1 = Match(name='my_partida', status='disponible',
               min_players=3, max_players=3, num_games=10, num_rounds=10,
               owner=User[user1])
    p1.players.add(Robot[robot1])
    p1.flush()
    return p1.id


@pytest.fixture
@db_session
def partida2(robot1, user1):
    p2 = Match(name='my_partida', password='leandro',
               status='disponible',
               min_players=3, max_players=3, num_games=10, num_rounds=10,
               owner=User[user1])
    p2.players.add(Robot[robot1])
    p2.flush()
    return p2.id


@pytest.fixture
@db_session
def partida3(user1):
    p3 = Match(name='my_partida', password='leandro',
               status='ocupada',
               min_players=3, max_players=3, num_games=10, num_rounds=10,
               owner=User[user1])
    p3.flush()
    return p3.id


@pytest.fixture
@db_session
def partida4(user1, robot2):
    p4 = Match(name='my_partida', password='leandro',
               status='disponible',
               min_players=3, max_players=3, num_games=10, num_rounds=10,
               owner=User[user1])
    p4.players.add(Robot[robot2])
    p4.flush()
    return p4.id


@pytest.fixture
@db_session
def partida5(user1, robot1, robot3):
    p5 = Match(name='my_partida', password='leandro',
               status='disponible',
               min_players=2, max_players=3, num_games=10, num_rounds=10,
               owner=User[user1])
    p5.players.add(Robot[robot1])
    p5.players.add(Robot[robot3])
    p5.flush()
    return p5.id


@pytest.fixture
@db_session
def partida6(user1, robot2, robot1):
    p5 = Match(name='my_partida', password='leandro',
               status='iniciada',
               min_players=2, max_players=2, num_games=10, num_rounds=10,
               owner=User[user1])
    p5.players.add(Robot[robot1])
    p5.players.add(Robot[robot2])
    p5.flush()
    return p5.id
