from pytest import raises, approx
from math import pi
from random import uniform as randfloat

from engine.vector import Vector


ZEROVEC = Vector((0, 0))


def test_vector_constructor():
    new = Vector(cartesian=(5, 20))
    assert new.x == approx(5)
    assert new.y == approx(20)
    new = Vector(polar=(pi, 10))
    assert new.angle == approx(pi)
    assert new.modulo == approx(10)


def test_vector_constructor_invalid():
    with raises(ValueError):
        Vector()
    with raises(ValueError):
        Vector(cartesian=(1, 2), polar=(3, 4))


def test_conversion():
    vec1 = Vector(cartesian=(3, 4))
    vec2 = Vector(polar=vec1.polar)
    vec3 = Vector(cartesian=vec2.cartesian)
    assert vec1 == vec2 == vec3


def test_directions():
    right_cartesian = Vector(cartesian=(10, 0))
    right_polar = Vector(polar=(0, 10))
    assert right_cartesian == right_polar
    assert right_polar.angle == approx(0)
    up_cartesian = Vector(cartesian=(0, 100))
    up_polar = Vector(polar=(pi / 2, 100))
    assert up_cartesian == up_polar
    assert up_polar.angle == approx(pi / 2)


def test_update():
    vec = Vector(cartesian=(15, 30))

    original_polar = vec.polar
    vec.cartesian = (-10, 5)
    assert vec.polar != original_polar

    new_cartesian = vec.cartesian
    vec.polar = original_polar
    assert vec.cartesian != new_cartesian


def test_bounds():
    minxy = Vector(cartesian=(-10e6, -10e6))
    maxxy = Vector(cartesian=(10e6, 10e6))
    vec = Vector(cartesian=(randfloat(-10e8, -10e6), randfloat(10e6, 10e8)))
    assert not vec.is_bounded(minxy, maxxy)
    new = vec.bound(minxy, maxxy)
    assert new.is_bounded(minxy, maxxy)


def test_add_mul_sub():
    vec = Vector(cartesian=(randfloat(-10e6, 10e6), randfloat(-10e6, 10e6)))
    doublevec = vec * 2
    assert vec + vec == doublevec
    assert vec == doublevec - vec
    assert vec - vec == ZEROVEC


def test_iadd():
    vec = Vector(cartesian=(randfloat(-10e6, 10e6), randfloat(-10e6, 10e6)))
    orig = Vector(cartesian=vec.cartesian)
    vec += vec
    assert vec == orig + orig


def test_distance():
    vec = Vector(cartesian=(randfloat(-10e6, 10e6), randfloat(-10e6, 10e6)))
    assert vec.distance(vec * -1) == (vec * -1).distance(vec) == 2 * vec.modulo


def test_both_mul():
    vec1 = Vector(cartesian=(3, 4))
    vec2 = Vector(polar=vec1.polar)
    factor = randfloat(-10e3, 10e3)
    assert vec1 * factor == vec2 * factor


def test_repr():
    vec1 = Vector(cartesian=(randfloat(-10e6, 10e6), randfloat(-10e6, 10e6)))
    vec2 = Vector(polar=(randfloat(pi * -1, pi), randfloat(-10e6, 10e6)))
    assert eval(repr(vec1)) == vec1
    assert eval(repr(vec2)) == vec2
