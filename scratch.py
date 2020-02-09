import solid as sc
import typing
import math
from euclid3 import Point2
import utils


import z3

circle_center = Point2(15, 15)
circle_radius = 10
circle = sc.translate((*circle_center, 0))(sc.circle(circle_radius, segments=100))

square = sc.square(20, center=True)


def dist_square(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


PRECISION = 6


def assert_tangent_to_circle(
    fillet_center, fillet_radius: float, circle_radius: Point2, circle_center: Point2
):
    dist_squared = (circle_center.x - fillet_center[0]) ** 2 + (
        circle_center.y - fillet_center[1]
    ) ** 2
    return dist_squared == (circle_radius + fillet_radius) ** 2


def assert_tangent_to_line(
    fillet_center, fillet_radius: float, line_point: Point2, line_angle: float,
):
    x, y = fillet_center
    line_angle = line_angle % 360.0
    if line_angle == 90 or line_angle == 270:
        return z3.Or(
            x == line_point.x + fillet_radius, x == line_point.x - fillet_radius,
        )

    line_angle = math.radians(line_angle)
    line_slope = math.tan(line_angle)
    line_intercept = line_point.y - (line_point.x * line_slope)
    intercept_offset = fillet_radius * math.cos(line_angle)

    return z3.Or(
        x * line_slope + line_intercept + intercept_offset == y,
        x * line_slope + line_intercept - intercept_offset == y,
    )


def solution_as_float(solution: z3.RatNumRef):
    as_str = solution.as_decimal(PRECISION)
    if as_str.endswith("?"):
        return float(as_str[:-1])
    return float(as_str)


def all_solutions_point2(solver: z3.Solver, fillet_center) -> typing.List[Point2]:
    solutions = []
    x, y = fillet_center
    while solver.check() == z3.sat:
        m = solver.model()
        solution = Point2(solution_as_float(m[x]), solution_as_float(m[y]))
        solutions.append(solution)
        solver.add(
            (x - solution.x) ** 2 + (y - solution.y) ** 2 > 10 ** (-PRECISION) * 100
        )
    return solutions


def choose_solution_in_direction(
    solutions: typing.List[Point2], direction_angle: float,
) -> Point2:
    def project(solution: Point2) -> float:
        angle = math.radians(utils.point_angle(solution) - direction_angle)
        return solution.magnitude() * math.cos(angle)

    return max(solutions, key=project)


def tangent_to_circle_and_line(
    fillet_radius: float,
    circle_radius: Point2,
    circle_center: Point2,
    line_point,
    line_angle,
    prefered_fillet_center_direction=None,
) -> typing.List[Point2]:
    fillet_center = z3.Reals("x y")
    solver = z3.Solver()
    solver.add(
        assert_tangent_to_circle(
            fillet_center, fillet_radius, circle_radius, circle_center
        )
    )
    solver.add(
        assert_tangent_to_line(fillet_center, fillet_radius, line_point, line_angle)
    )
    solutions = all_solutions_point2(solver, fillet_center)
    if prefered_fillet_center_direction is None:
        return solutions
    else:
        return choose_solution_in_direction(solutions, prefered_fillet_center_direction)


solutions = tangent_to_circle_and_line(3, 10, Point2(15, 15), Point2(10, 0), 90)

tangent_circles = sc.union()(
    [sc.translate((*pos, 0))(sc.circle(3, segments=100)) for pos in solutions]
)

preferred_solution = choose_solution_in_direction(solutions, -45)

preferred_tangent_circle = sc.translate((*preferred_solution, 0))(sc.circle(3, segments=100))

print("preferred: ", preferred_solution)

d = circle + square
# d = (d - tangent_circles) + (tangent_circles - d)
d = sc.color("red")(preferred_tangent_circle) + d


sc.scad_render_to_file(d, "/tmp/output.scad")
