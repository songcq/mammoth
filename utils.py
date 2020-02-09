import solid
import math
from euclid3 import Point2

big_cutter_length = 20
big_cutter_square = solid.square(big_cutter_length * 2, center=True)


def rotate_around_point(obj, angle, vector, point):
    neg_point = tuple(-x for x in point)
    obj = solid.translate(neg_point)(obj)
    obj = solid.rotate(angle, vector)(obj)
    return solid.translate(point)(obj)


def unit_point2(degrees) -> Point2:
    rad = math.radians(degrees)
    return Point2(math.cos(rad), math.sin(rad))


def _circle_center_by_three_points(p0: Point2, p1: Point2, p2: Point2) -> Point2:
    yd_b = p2[1] - p1[1]
    xd_b = p2[0] - p1[0]
    yd_a = p1[1] - p0[1]
    xd_a = p1[0] - p0[0]
    a_s = yd_a / xd_a
    b_s = yd_b / xd_b
    cex = (
        a_s * b_s * (p0[1] - p2[1]) + b_s * (p0[0] + p1[0]) - a_s * (p1[0] + p2[0])
    ) / (2 * (b_s - a_s))
    cey = -1 * (cex - (p0[0] + p1[0]) / 2) / a_s + (p0[1] + p1[1]) / 2
    return Point2(cex, cey)


def three_point_cicle(p0: Point2, p1: Point2, p2: Point2, radius_adjustment=0):
    center = _circle_center_by_three_points(p0, p1, p2)
    radius = ((center[0] - p0[0]) ** 2 + (center[1] - p0[1]) ** 2) ** 0.5
    return solid.translate((center[0], center[1], 0))(
        solid.circle(radius + radius_adjustment, segments=100)
    )

def point_angle(a: Point2):
    angle = math.degrees(math.acos(a.x / a.magnitude()))
    if a.y < 0:
        angle = - angle
    return angle
