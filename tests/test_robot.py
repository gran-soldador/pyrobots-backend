from engine.robot import BotCommands, Robot, MAXSPEED, MAXX, MAXY, INERTIA
from engine.vector import Vector
from math import isclose, degrees, sqrt
from copy import deepcopy
import pytest
from pytest import approx


class EmptyBot(Robot):
    def initialize(self):
        pass

    def respond(self):
        pass


def test_incomplete_robot():
    class IncompleteRobot(Robot):
        pass

    rut = IncompleteRobot()
    rut._initialize_or_die()
    assert rut.get_damage() == 100
    rut = IncompleteRobot()
    rut._respond_or_die()
    assert rut.get_damage() == 100


def test_do_nothing_robot():
    rut = EmptyBot()
    initial_status = deepcopy(rut._status)
    initial_status.cannon_cooldown = -10
    rut._initialize_or_die()
    for _ in range(10):
        rut._respond_or_die()
        rut._execute_cannon()
        rut._execute_drive()
    assert initial_status == rut._status
    assert rut._commands == BotCommands()


def test_moving_robot():
    class MovingRobot(EmptyBot):
        def respond(self):
            self.drive(90, 100)

    rut = MovingRobot()
    rut._status.position = Vector(cartesian=(.5 * MAXX, .5 * MAXY))
    rut._initialize_or_die()
    rut._respond_or_die()
    rut._execute_cannon()
    rut._execute_drive()
    x, y = rut.get_position()
    assert isclose(x, .5 * MAXX, rel_tol=INERTIA)
    assert isclose(y, .5 * MAXY + MAXSPEED, rel_tol=INERTIA)
    assert rut.get_direction() == approx(90)
    assert isclose(rut.get_velocity(), 100, rel_tol=INERTIA)


def test_moving_twice_robot():
    class MovingTwiceRobot(EmptyBot):
        def respond(self):
            self.drive(180, 50)
            self.drive(0, 25)

    rut = MovingTwiceRobot()
    rut._status.position = Vector(cartesian=(.5 * MAXX, .5 * MAXY))
    rut._initialize_or_die()
    rut._respond_or_die()
    rut._execute_cannon()
    rut._execute_drive()
    x, y = rut.get_position()
    assert isclose(x, .5 * MAXX + 25 / 100 * MAXSPEED, rel_tol=INERTIA)
    assert isclose(y, .5 * MAXY, rel_tol=INERTIA)
    assert rut.get_direction() == approx(0)
    assert isclose(rut.get_velocity(), 25, rel_tol=INERTIA)


def test_moving_oob_robot():
    class MovingOOBRobot(EmptyBot):
        def respond(self):
            self.drive(0, 100)

    rut = MovingOOBRobot()
    rut._status.position = Vector(cartesian=(.999 * MAXX, .999 * MAXY))
    rut._initialize_or_die()
    rut._respond_or_die()
    rut._execute_cannon()
    rut._execute_drive()
    x, y = rut.get_position()
    assert isclose(x, MAXX)
    assert isclose(y, .999 * MAXY)
    assert rut.get_damage() == 2


@pytest.mark.parametrize("angle, velocity", [(0, 150), (-10, 25)])
def test_invalid_drive_robot(angle, velocity):
    class InvalidRobot(EmptyBot):
        def respond(self):
            self.drive(angle, velocity)

    rut = InvalidRobot()
    rut._initialize_or_die()
    rut._respond_or_die()
    rut._execute_cannon()
    rut._execute_drive()
    assert rut.get_damage() == 100


def test_turning_too_fast_robot():
    class TurningTooFastRobot(Robot):
        def initialize(self):
            self.first = True

        def respond(self):
            if self.first:
                self.drive(90, 100)
            else:
                self.drive(270, 100)
            self.first = False

    rut = TurningTooFastRobot()
    rut._status.position = Vector(cartesian=(.5 * MAXX, .5 * MAXY))
    Robot._initialize_or_die(rut)
    Robot._respond_or_die(rut)
    Robot._execute_drive(rut)
    assert rut.get_damage() == 0
    Robot._respond_or_die(rut)
    Robot._execute_drive(rut)
    assert rut.get_damage() == 100


def test_cannon_robot():
    class CannonRobot(EmptyBot):
        def respond(self):
            self.cannon(90, 100)

    rut = CannonRobot()
    rut._initialize_or_die()
    rut._respond_or_die()
    missile = rut._execute_cannon()
    rut._execute_drive()
    assert rut._commands.cannon_degree == 90
    assert rut._commands.cannon_distance == 100
    assert rut._commands.cannon_used is True
    assert degrees(missile.angle) == approx(90)
    assert missile.modulo == approx(100)
    assert rut._status.cannon_cooldown >= 2

    rut._respond_or_die()
    missile = rut._execute_cannon()
    rut._execute_drive()
    assert missile is None
    assert rut._status.damage == 100


@pytest.mark.parametrize(
    "degree, distance",
    [(90, -150), (-10, 25), (0, 1000)])
def test_invalid_cannon_robot(degree, distance):
    class InvalidRobot(EmptyBot):
        def respond(self):
            self.cannon(degree, distance)

    rut = InvalidRobot()
    rut._initialize_or_die()
    rut._respond_or_die()
    rut._execute_cannon()
    rut._execute_drive()
    assert rut.get_damage() == 100


@pytest.mark.parametrize(
    "direction, resolution, found",
    [(54, 20, True), (45, 5, True), (180, 20, False), (0, 20, False)])
def test_scanner_robot(direction, resolution, found):
    class ScannerRobot(EmptyBot):
        def respond(self):
            self.point_scanner(direction, resolution)

    rut = ScannerRobot()
    rut._status.position = Vector(cartesian=(500, 500))
    others = [Vector(cartesian=(600, 600)), Vector(cartesian=(700, 700))]
    distance = approx(sqrt(2) * 100)
    rut._initialize_or_die()
    rut._respond_or_die()
    rut._execute_cannon()
    rut._execute_scanner(others)
    rut._execute_drive()
    assert degrees((others[0] - rut._status.position).angle) == approx(45)
    assert rut._commands.scanner_direction == direction
    assert rut._commands.scanner_resolution == resolution
    assert rut._commands.scanner_used is True
    assert rut.scanned() == (distance if found else None)


@pytest.mark.parametrize("direction, resolution",
                         [(90, -150), (-10, 25), (370, 359), (15, 400)])
def test_invalid_scanner_robot(direction, resolution):
    class InvalidRobot(EmptyBot):
        def respond(self):
            self.point_scanner(direction, resolution)

    rut = InvalidRobot()
    rut._initialize_or_die()
    rut._respond_or_die()
    rut._execute_cannon()
    rut._execute_scanner([Vector(cartesian=(10, 20))])
    rut._execute_drive()
    assert rut.get_damage() == 100
