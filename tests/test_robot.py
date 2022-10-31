from engine.robot import Robot, MAXSPEED, MAXX, MAXY, INERTIA
from engine.vector import Vector
from math import isclose
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
    class InvalidSpeedRobot(EmptyBot):
        def respond(self):
            self.drive(angle, velocity)

    rut = InvalidSpeedRobot()
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
