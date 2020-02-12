import solid as sc
from euclid3 import Point2

import switches
from switches import mm


def get_scew_positions():
    def create(addr, corner):
        addr, corner = Point2(*addr), Point2(*corner)
        pos = switches.get_cap_corner(addr, corner)
        return pos

    thumb_fan_size = switches.thumb_fan_size
    holes = [
        # top
        ((0, 3), (-0.5, 0.5 - 2 * mm)),
        ((2, 3), (0.5, 0.5)),
        ((4, 3), (0.5, 0.5 - 2 * mm)),
        # mid
        # ((0, 2), (-0.5, 0)),
        # ((1, 2), (0.5, 0)),
        # ((3, 2), (-0.5, 0)),
        # ((4, 2), (0.5, 0)),
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
    return [create(*arg) for arg in holes]


def create_screws(diameter=2.1 * mm):
    holes = [
        sc.translate((*pos, 0))(sc.circle(d=diameter, segments=30))
        for pos in get_scew_positions()
    ]
    return sc.union()(holes)
