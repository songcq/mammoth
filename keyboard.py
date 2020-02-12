import solid as sc
from euclid3 import Point2
import tabulate

# import z3
import switches
import case
import screws
from switches import mm, switch_size

sc.SEGMENTS = 100


case = case.create_case()

screws_holes = screws.create_screws()

switch_plate = case - switches.create_all_switches(size=switch_size) - screws_holes

buttom_plate = case - screws_holes


d = sc.linear_extrude(1.5 * mm)(switch_plate)
d = d + sc.utils.up(-6 * mm)(sc.linear_extrude(1.5 * mm)(buttom_plate))
d = sc.color("silver")(d) + switches.create_all_caps()

# d = switch_plate

# d = case - (sc.offset(-2 * mm)(case))
# d = d + screws.create_screws(diameter=5 * mm) - screws.create_screws(diameter=3 * mm)
# d = (d - switches.create_all_switches()) + (
#     switches.create_all_switches() - d
# )

sc.scad_render_to_file(d, "/tmp/output.scad")


def print_stats():
    table = []

    p0 = switches.get_cap_corner((1, 0), Point2(0.001, 0))
    p1 = switches.get_cap_corner((2, 0), Point2(0.001, 0))
    table.append(["thumb_switch_distance", (p0.distance(p1)) * 19.05])

    p0 = switches.get_cap_corner((1, 0), Point2(switch_size / 2, -switch_size / 2))
    p1 = switches.get_cap_corner((2, 0), Point2(-switch_size / 2, -switch_size / 2))
    table.append(["thumb_switch_lower_corner_distance", (p0.distance(p1)) * 19.05])

    p0 = switches.get_cap_corner((1, 0), Point2(0.5, 0.5))
    p1 = switches.get_cap_corner((2, 0), Point2(-0.5, 0.5))
    table.append(["thumb_cap_upper_corner_distance", (p0.distance(p1)) * 19.05])

    p0 = switches.get_cap_corner((0, 1), Point2(-0.5, 0))
    p1 = switches.get_cap_corner((switches.thumb_fan_size - 1, 0), Point2(0.5, 0.5))
    table.append(["total_width", p1.x - p0.x])

    print(tabulate.tabulate(table))


print_stats()
