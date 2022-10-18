from engine.robot import Position, Robot, MAXSPEED, MAXX, MAXY
from math import isclose
from copy import deepcopy
import pytest


def test_cheating_robot():
    class CheatingRobot(Robot):
        def initialize(self):
            self._status.damage = 1.1

        def respond(self):
            self._status.damage = 1.1

    rut = CheatingRobot()
    Robot._initialize_or_die(rut)
    assert rut._status.damage == 100
    rut = CheatingRobot()
    Robot._respond_or_die(rut)
    assert rut._status.damage == 100


def test_incomplete_robot():
    class IncompleteRobot(Robot):
        pass

    rut = IncompleteRobot()
    Robot._initialize_or_die(rut)
    assert rut._status.damage == 100
    rut = IncompleteRobot()
    Robot._respond_or_die(rut)
    assert rut._status.damage == 100


def test_do_nothing_robot():
    class LazyRobot(Robot):
        def initialize(self):
            pass

        def respond(self):
            pass

    rut = LazyRobot()
    initial_status = deepcopy(rut._status)
    Robot._initialize_or_die(rut)
    for _ in range(10):
        Robot._respond_or_die(rut)
        Robot._execute_drive(rut)
    assert initial_status == rut._status


def test_moving_robot():
    class MovingRobot(Robot):
        def initialize(self):
            pass

        def respond(self):
            self.drive(90, 100)

    rut = MovingRobot()
    rut._status.position = Position(.5 * MAXX, .5 * MAXY)
    Robot._initialize_or_die(rut)

    Robot._respond_or_die(rut)
    Robot._execute_drive(rut)
    assert isclose(rut._status.position.x, .5 * MAXX)
    assert isclose(rut._status.position.y, .5 * MAXY + MAXSPEED)


def test_moving_twice_robot():
    class MovingTwiceRobot(Robot):
        def initialize(self):
            pass

        def respond(self):
            self.drive(180, 50)
            self.drive(0, 25)

    rut = MovingTwiceRobot()
    rut._status.position = Position(.5 * MAXX, .5 * MAXY)
    Robot._initialize_or_die(rut)

    Robot._respond_or_die(rut)
    Robot._execute_drive(rut)
    assert isclose(rut._status.position.x, .5 * MAXX + 25 / 100 * MAXSPEED)
    assert isclose(rut._status.position.y, .5 * MAXY)


def test_moving_oob_robot():
    class MovingOOBRobot(Robot):
        def initialize(self):
            pass

        def respond(self):
            self.drive(0, 100)

    rut = MovingOOBRobot()
    rut._status.position = Position(.999 * MAXX, .999 * MAXY)
    Robot._initialize_or_die(rut)

    Robot._respond_or_die(rut)
    Robot._execute_drive(rut)
    assert isclose(rut._status.position.x, MAXX)
    assert isclose(rut._status.position.y, .999 * MAXY)
    assert rut._status.damage == 2


def test_invalid_speed_robot():
    class InvalidSpeedRobot(Robot):
        def initialize(self):
            pass

        def respond(self):
            self.drive(0, 150)

    rut = InvalidSpeedRobot()
    Robot._initialize_or_die(rut)
    with pytest.raises(ValueError):
        Robot._respond_or_die(rut)
        Robot._execute_drive(rut)


def test_invalid_angle_robot():
    class InvalidAngleRobot(Robot):
        def initialize(self):
            pass

        def respond(self):
            self.drive(-10, 25)

    rut = InvalidAngleRobot()
    Robot._initialize_or_die(rut)
    with pytest.raises(ValueError):
        Robot._respond_or_die(rut)
        Robot._execute_drive(rut)


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
    rut._status.position = Position(.5 * MAXX, .5 * MAXY)
    Robot._initialize_or_die(rut)
    Robot._respond_or_die(rut)
    Robot._execute_drive(rut)
    with pytest.raises(ValueError):
        Robot._respond_or_die(rut)
        Robot._execute_drive(rut)
