import solid as sc
import solid.utils as scu
import math
import typing
from euclid3 import Point2

import utils

mm = 1 / 19.05
switch_size = 14 * mm

virtical_col_offsets = [-0.75, -0.25, 0, -0.25, -0.37]
thumb_fan_size = 4

all_switch_addresses: typing.List[Point2] = (
    [(col, row) for row in range(1, 4) for col in range(5)]
    + [(col, 0) for col in range(thumb_fan_size)]
)


def get_switch_angle(addr: Point2) -> float:
    if addr[1] >= 1:
        return 0
    else:
        return -(1 + addr[0]) * 11.25


def get_switch_position(addr: Point2) -> Point2:
    col, row = addr
    if row >= 1:
        x = col
        y = row + virtical_col_offsets[col]
    else:
        x = 2.5
        y = -0.3
        thumb_row_radiuss = 4.5
        switch_angle = -get_switch_angle((col, row)) / 180 * math.pi
        x += math.sin(switch_angle) * thumb_row_radiuss
        y -= (1 - math.cos(switch_angle)) * thumb_row_radiuss

    return Point2(x, y)


def create_cap(char=None):
    cap = sc.square(0.975, center=True)
    cap = scu.up(3 * mm)(cap)
    cap = sc.linear_extrude(height=0.95, scale=0.6)(cap)
    cutter = sc.sphere(r=3, segments=50)
    cutter = scu.up(3.5)(cutter)
    cap = cap - cutter
    cap = sc.color("gray")(cap)
    if char is not None:
        char = sc.text(char, size=0.25, segments=20, halign="center", valign="center")
        char = sc.linear_extrude(height=1, convexity=3)(char)
        char = sc.color("red")(cap * char)
        char = scu.up(1 * mm)(char)
        cap = cap - char + char
    return cap


def create_all_caps():
    # text = "ABCDEFGHIJKLMNOPQRST"

    def create(i):
        # cap = create_cap(text[i])
        cap = create_cap()
        addr = all_switch_addresses[i]
        i += 1
        pos = get_switch_position(addr)
        angle = get_switch_angle(addr)
        cap = sc.rotate(angle, scu.UP_VEC)(cap)
        cap = sc.translate((*pos, 3 * mm))(cap)
        return cap

    return sc.union()([create(i) for i in range(len(all_switch_addresses))])


def create_switch(addr, size=switch_size):
    pos = get_switch_position(addr)
    angle = get_switch_angle(addr)
    cap = scu.square(size, center=True)()
    cap = sc.rotate(angle, scu.UP_VEC)(cap)
    cap = sc.translate((*pos, 0))(cap)
    return cap


def get_cap_corner(addr: Point2, corner: Point2) -> Point2:
    angle = get_switch_angle(addr)
    pos = get_switch_position(addr)
    if angle == 0:
        return pos + corner

    angle += utils.point_angle(corner)
    offset = utils.unit_point2(angle) * corner.magnitude()
    return pos + offset


def create_all_switches(size=switch_size):
    return sc.union()([create_switch(addr, size=size) for addr in all_switch_addresses])
