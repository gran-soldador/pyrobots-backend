from pony.orm import *
import sys

db = Database()

if "pytest" in sys.modules:
    db.bind(provider="sqlite", filename=":sharedmemory:")  # pragma: no cover
else:
    db.bind(provider="sqlite", filename="main.db",
            create_db=True)  # pragma: no cover


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 255, unique=True)
    email = Required(str, 255, unique=True)
    password = Required(str, 255)
    avatar = Optional(str, 255)
    verified = Required(bool)
    robots = Set('Robot', reverse='user')
    matches = Set('Match', reverse='owner')


class Robot(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 255)
    code = Required(str)
    avatar = Optional(str, 255)
    matches_num_won = Required(int)
    matches_num_played = Required(int)
    games_won = Required(int)
    rounds_won = Required(int)
    defective = Required(bool)
    plays_in = Set('Match', reverse='players')
    user = Required(User, reverse='robots')
    won_in = Set('Match', reverse='winner')


class Match(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 32)
    password = Optional(str, 10, nullable=True, default=None)
    status = Required(str, 32)
    min_players = Required(int)
    max_players = Required(int)
    num_games = Required(int)
    num_rounds = Required(int)
    players = Set(Robot, reverse='plays_in')
    owner = Required(User, reverse='matches')
    winner = Set(Robot, reverse='won_in')


db.generate_mapping(create_tables=True)
