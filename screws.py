import solid as sc
import enum
import typing
from euclid3 import Point2

import switches
from switches import mm


class Screw_Position(enum.Enum):
    In_case_wall = 0
    Interior = 1


def get_scew_positions(screw_position: Screw_Position) -> typing.List[Point2]:
    def create(addr, corner):
        addr, corner = Point2(*addr), Point2(*corner)
        pos = switches.get_cap_corner(addr, corner)
        return pos

    thumb_fan_size = switches.thumb_fan_size
    if screw_position == Screw_Position.In_case_wall:
        holes = [
            # top
            ((0, 3), (-0.5, 0.5 - 2 * mm)),
            ((2, 3), (0.5, 0.5)),
            ((4, 3), (0.5, 0.5 - 2 * mm)),
            # mid
            # ((1, 2), (-0.5, -0.25)),
            # ((2, 2), (0, -0.5)),
            # ((4, 2), (-0.5, 0)),
            # # bottom
            ((0, 1), (-0.5, -0.5)),
            ((2, 1), (0, -0.5 - 2 * mm)),
            ((4, 1), (0.5, -0.5)),
            # thumb fan
            # ((0, 0), (-0.5, 0.5)),
            ((0, 0), (-0.5, -0.5)),
            ((thumb_fan_size - 2, 0), (0, 0.5)),
            ((thumb_fan_size - 2, 0), (0, -0.5)),
            ((thumb_fan_size - 1, 0), (0.5, 0.5)),
            ((thumb_fan_size - 1, 0), (0.5, -0.5)),
        ]
    elif screw_position == Screw_Position.Interior:
        holes = [
            # top
            ((0, 3), (0, 0.5)),
            ((2, 3), (0, -0.5)),
            ((4, 3), (0, 0.5)),

            # bottom
            ((0, 1), (0.5, 0)),
            ((2, 1), (0, -0.5)),
            # ((4, 1), (0, -0.5)),

            # thumb fan
            ((0, 0), (0, -0.5)),
            ((1, 0), (0, 0.5)),
            ((3, 0), (0, 0.5)),
            ((3, 0), (0, -0.5)),
        ]
    return [create(*arg) for arg in holes]


def create_screws(screw_position=Screw_Position.In_case_wall, diameter=2.1 * mm):
    holes = [
        sc.translate((*pos, 0))(sc.circle(d=diameter, segments=30))
        for pos in get_scew_positions(screw_position)
    ]
    return sc.union()(holes)
