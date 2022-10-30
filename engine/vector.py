from typing import Tuple
from math import cos, sin, atan2, sqrt, isclose
from .constants import EPSILON


Pair = Tuple[float, float]


class Vector:
    def __init__(self, cartesian: Pair = None, polar: Pair = None):
        """Vector supporting cartesian and polar coordinates

        Exactly one argument must be provided
        :param cartesian: (x, y) pair
        :param polar: (angle, modulo) pair
        """
        arg_count = sum(1 for i in [cartesian, polar] if i is not None)
        if arg_count != 1:
            raise ValueError(
                f"Must supply exactly 1 argument, supplied {arg_count}")
        self._cartesian = cartesian
        self._polar = polar

    @property
    def cartesian(self) -> Pair:
        if self._cartesian is None:
            angle, modulo = self._polar
            self._cartesian = (cos(angle) * modulo, sin(angle) * modulo)
        return self._cartesian

    @cartesian.setter
    def cartesian(self, val: Pair):
        self._cartesian = val
        self._polar = None

    @property
    def polar(self):
        if self._polar is None:
            x, y = self._cartesian
            self._polar = (atan2(y, x), sqrt(x**2 + y**2))
        return self._polar

    @polar.setter
    def polar(self, val: Pair):
        self._polar = val
        self._cartesian = None

    @property
    def x(self) -> float:
        return self.cartesian[0]

    @property
    def y(self) -> float:
        return self.cartesian[1]

    @property
    def angle(self) -> float:
        return self.polar[0]

    @property
    def modulo(self) -> float:
        return self.polar[1]

    def is_bounded(self, minxy, maxxy) -> bool:
        """ Test whether Vector is inside rectangle

        :param minxy: corner with minimum x and minimum y
        :param maxxy: corner with maximum x and maximum y
        :return: True iff self is inside rectangle defined by minxy, maxxy
        """
        return ((minxy.x <= self.x <= maxxy.x) and
                (minxy.y <= self.y <= maxxy.y))

    def bound(self, minxy, maxxy):
        """ Used to ensure Vector is inside rectangle

        :param minxy: corner with minimum x and minimum y
        :param maxxy: corner with maximum x and maximum y
        :return: New Vector such that it lies within rectangle
        """
        x = min(maxxy.x, max(minxy.x, self.x))
        y = min(maxxy.y, max(minxy.y, self.y))
        return Vector(cartesian=(x, y))

    def __eq__(self, other):
        x_eq = isclose(self.x, other.x, abs_tol=EPSILON)
        y_eq = isclose(self.y, other.y, abs_tol=EPSILON)
        return x_eq and y_eq

    def __add__(self, other):
        return Vector(cartesian=(self.x + other.x, self.y + other.y))

    def __iadd__(self, other):
        self.cartesian = (self.x + other.x, self.y + other.y)
        return self

    def __mul__(self, scalar: float):
        if self._cartesian is not None:
            return Vector(cartesian=(self.x * scalar, self.y * scalar))
        else:
            return Vector(polar=(self.angle, self.modulo * scalar))

    def __repr__(self):
        if self._cartesian is not None:
            return f"Vector(cartesian={self._cartesian})"
        else:
            return f"Vector(polar={self._polar})"
