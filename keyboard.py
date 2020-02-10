import solid as sc
from euclid3 import Point2

# import z3
import switches
import case
from switches import mm, switch_size

def create_screws():
    radius = 2.1 * mm / 2

    def create(addr, corner, adjustment=(0, 0)):
        addr, corner = Point2(*addr), Point2(*corner)
        pos = switches.get_cap_corner(addr, corner) + adjustment
        hole = sc.circle(radius, segments=20)
        hole = sc.translate((*pos, 0))(hole)
        return hole

    thumb_fan_size = switches.thumb_fan_size
    holes = [
        # top
        ((0, 3), (-0.5, 0.5), (0, -2 * mm)),
        ((2, 3), (0, 0.5)),
        ((4, 3), (0.5, 0.5), (0, -2 * mm)),
        # bottom
        ((0, 1), (-0.5, -0.5)),
        ((2, 1), (0, -0.5), (0, -2.5 * mm)),
        ((4, 1), (0.5, -0.5), (1.5*mm, 1.5*mm)),
        # thumb fan
        ((0, 0), (-0.5, -0.5)),
        ((thumb_fan_size - 2, 0), (0, 0.5)),
        ((thumb_fan_size - 2, 0), (0, -0.5)),
        ((thumb_fan_size - 1, 0), (0.5, 0.5)),
        ((thumb_fan_size - 1, 0), (0.5, -0.5)),
    ]
    holes = [create(*arg) for arg in holes]
    return sc.union()(holes)


case = case.create_case()

switch_plate = case - switches.create_all_switches(size=switch_size) - create_screws()

buttom_plate = case - create_screws()

d = sc.linear_extrude(1.5 * mm)(switch_plate)
# d = d + sc.utils.up(-6 * mm)(sc.linear_extrude(1.5 * mm)(buttom_plate))
d = sc.color("silver")(d) + switches.create_all_caps()

sc.scad_render_to_file(d, "/tmp/output.scad")

p0 = switches.get_cap_corner((1, 0), Point2(0.001, 0))
p1 = switches.get_cap_corner((2, 0), Point2(0.001, 0))
print((p0.distance(p1)) * 19.05)

p0 = switches.get_cap_corner((1, 0), Point2(switch_size/2, -switch_size/2))
p1 = switches.get_cap_corner((2, 0), Point2(-switch_size/2, -switch_size/2))
print((p0.distance(p1)) * 19.05)
