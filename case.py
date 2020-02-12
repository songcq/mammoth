import solid as sc
import solid.utils as scu
from euclid3 import Point2, Point3

import switches
import utils

from switches import mm


def create_upper_case():
    p0 = switches.get_switch_position((0, 3)) + Point2(-0.5, 0.5)
    p1 = switches.get_switch_position((2, 3)) + Point2(-0.5, 0.5)
    p2 = switches.get_switch_position((4, 3)) + Point2(0.5, 0.5)
    case = utils.three_point_cicle(
        p0, p1, p2, radius_adjustment=-1.5 * mm, segments=1000
    )
    # cut left edge
    case = case * sc.translate((utils.big_cutter_length - 0.5, 0, 0))(
        utils.big_cutter_square
    )
    # cut right edge
    case = case * sc.translate((-utils.big_cutter_length + 4.5, 0, 0))(
        utils.big_cutter_square
    )
    # cut buttom edge
    _, buttom_left_switch_y = switches.get_switch_position((0, 1))
    case = case * sc.translate(
        (0, utils.big_cutter_length + buttom_left_switch_y - 0.5, 0)
    )(utils.big_cutter_square)
    return case


def create_thumb_fan():
    p0 = switches.get_switch_position((0, 0))
    p1 = switches.get_switch_position((2, 0))
    p2 = switches.get_switch_position((4, 0))
    outer_cicle = utils.three_point_cicle(
        p0, p1, p2, radius_adjustment=0.5, segments=1000
    )
    inner_cicle = utils.three_point_cicle(
        p0, p1, p2, radius_adjustment=-0.5, segments=1000
    )
    ring = outer_cicle - inner_cicle
    # rough cut left edge
    ring = ring * sc.translate((utils.big_cutter_length + p0.x - 0.5 - 2.5 * mm, 0, 0))(
        utils.big_cutter_square
    )
    # rough cut right edge
    ring = ring * sc.translate((0, utils.big_cutter_length - 3.5, 0))(
        utils.big_cutter_square
    )
    # cut parallel to 1st and last switches

    def create_cutter(addr, left_or_right_dir):
        pos = switches.get_switch_position(addr)
        pos = Point3(*pos, 0)
        angle = switches.get_switch_angle(addr)
        cutter = switches.create_switch(addr, size=1)
        cutter = sc.translate(pos)(sc.scale((4, 4, 0))(sc.translate(pos * -1)(cutter)))
        offset = utils.unit_point2(angle) * 2.5 * left_or_right_dir
        cutter = sc.translate((*offset, 0))(cutter)
        return cutter

    ring = ring - (create_cutter(Point2(0, 0), -1))
    ring = ring - (create_cutter(Point2(switches.thumb_fan_size - 1, 0), 1))
    return ring


def create_left_buttom_circle():
    p0 = switches.get_cap_corner((0, 1), Point2(0.5, -0.5))
    p1 = switches.get_cap_corner((1, 1), Point2(0.5, -0.55))
    p2 = switches.get_cap_corner((3, 1), Point2(0, -0.575))
    circle = utils.three_point_cicle(
        p0, p1, p2, radius_adjustment=1.5 * mm, segments=1000
    )
    right_edge = switches.get_cap_corner(Point2(0, 0), Point2(-0.5, 0.5)).x
    return circle * sc.square(right_edge * 2, center=True)


def create_case():
    case = create_upper_case()
    case = case - create_left_buttom_circle()
    case = case + create_thumb_fan()
    case = sc.offset(r=15 * mm, segments=100)(case)
    case = sc.offset(r=-12.5 * mm, segments=100)(case)
    return case
