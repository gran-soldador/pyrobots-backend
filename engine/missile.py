from dataclasses import dataclass, field

from .vector import Vector
from .constants import MISSILE_SPEED


@dataclass(order=True)
class MissileInFlight:
    hit_round: int
    start_round: int = field(compare=False)
    origin: Vector = field(compare=False)
    destination: Vector = field(compare=False)
    angle: float = field(compare=False)
    sender: int = field(compare=False)

    def curr_pos(self, round: int) -> Vector:
        movement = Vector(polar=(
            self.angle,
            (round - self.start_round) * MISSILE_SPEED
        ))
        return self.origin + movement
