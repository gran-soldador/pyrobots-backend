from math import cos, sin, atan2, sqrt, isclose
from .constants import EPSILON


Pair = tuple[float, float]


class Vector:
    __slots__ = ["x", "y"]

    def __init__(self, cartesian: Pair = None, polar: Pair = None):
        """Vector supporting cartesian and polar coordinates

        Exactly one argument must be provided
        :param cartesian: (x, y) pair
        :param polar: (angle, modulo) pair
        """
        if (cartesian is None) == (polar is None):
            raise ValueError("Must supply exactly 1 argument")
        if cartesian is not None:
            self.x, self.y = cartesian
        else:
            self.polar = polar

    @property
    def cartesian(self) -> Pair:
        return (self.x, self.y)

    @cartesian.setter
    def cartesian(self, val: Pair):
        self.x, self.y = val

    @property
    def polar(self):
        return (atan2(self.y, self.x), sqrt(self.x**2 + self.y**2))

    @polar.setter
    def polar(self, val: Pair):
        angle, modulo = val
        self.x, self.y = (cos(angle) * modulo, sin(angle) * modulo)

    @property
    def angle(self) -> float:
        return atan2(self.y, self.x)

    @property
    def modulo(self) -> float:
        return sqrt(self.x**2 + self.y**2)

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

    def distance(self, other) -> float:
        return (self - other).modulo

    def __eq__(self, other):
        x_eq = isclose(self.x, other.x, abs_tol=EPSILON)
        y_eq = isclose(self.y, other.y, abs_tol=EPSILON)
        return x_eq and y_eq

    def __add__(self, other):
        return Vector(cartesian=(self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Vector(cartesian=(self.x - other.x, self.y - other.y))

    def __iadd__(self, other):
        self.x, self.y = (self.x + other.x, self.y + other.y)
        return self

    def __mul__(self, scalar: float):
        return Vector(cartesian=(self.x * scalar, self.y * scalar))

    def __repr__(self):
        return f"Vector(cartesian={(self.x, self.y)})"
