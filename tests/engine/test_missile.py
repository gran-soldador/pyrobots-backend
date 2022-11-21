from engine.vector import Vector
from engine.missile import MissileInFlight
from engine.constants import MISSILE_SPEED


def test_missile_curr_pos():
    destination_x = 8.5 * MISSILE_SPEED
    missile = MissileInFlight(
        10,
        1,
        Vector(cartesian=(0, 0)),
        Vector(cartesian=(destination_x, 0)),
        0,
        10
    )
    poss = [missile.curr_pos(round) for round in range(1, 16)]
    for prev, curr in zip(poss, poss[1:]):
        assert prev.x <= curr.x
        assert curr.x <= destination_x
