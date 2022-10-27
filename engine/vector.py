from typing import Tuple
from math import cos, sin, atan2, sqrt, isclose


class Vector:
    def __init__(self,
                 *,
                 cartesian: Tuple[float, float] = None,
                 polar: Tuple[float, float] = None):
        arg_count = sum(1 for i in [cartesian, polar] if i is not None)
        if arg_count != 1:
            raise ValueError(
                f"Must supply exactly 1 argument, supplied {arg_count}")
        self._cartesian = cartesian
        self._polar = polar

    @property
    def cartesian(self):
        if self._cartesian is not None:
            return self._cartesian
        angle, modulo = self._polar
        return (cos(angle) * modulo, sin(angle) * modulo)

    @cartesian.setter
    def cartesian(self, val):
        self._cartesian = val
        self._polar = None

    @property
    def polar(self):
        if self._polar is not None:
            return self._polar
        x, y = self._cartesian
        return (atan2(x, y), sqrt(x**2 + y**2))

    @polar.setter
    def polar(self, val):
        self._polar = val
        self._cartesian = None

    @property
    def x(self):
        return self.cartesian[0]

    @property
    def y(self):
        return self.cartesian[1]

    @property
    def angle(self):
        return self.polar[0]

    @property
    def modulo(self):
        return self.polar[1]

    def __eq__(self, other):
        x_eq = isclose(self.x, other.x, rel_tol=1e-7)
        y_eq = isclose(self.y, other.y, rel_tol=1e-7)
        return x_eq and y_eq

    def __add__(self, other):
        return Vector(cartesian=(self.x + other.x, self.y + other.y))

    def __iadd__(self, other):
        self.cartesian = (self.x + other.x, self.y + other.y)
        return self

    def __mul__(self, scalar):
        if self._cartesian is not None:
            return Vector(cartesian=(self.x * scalar, self.y * scalar))
        else:
            return Vector(polar=(self.angle, self.modulo * scalar))
