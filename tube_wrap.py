import solid as sc
import math
from solid.utils import Point2

import utils


def f(x):
    l = x
    a = x
    p = Point2(math.cos(a), math.sin(a))
    p.set_length(l)
    return p


points = [f(i * 0.3) for i in range(100)]

# d = _sp.catmull_rom_polygon(points, subdivisions=10)
d = sc.text("hi", halign="center", valign="center")


def wrap_tube(objects, radius, hstep, vstep):
    tilt_angle = utils.point_angle(Point2(hstep, vstep))

    def create(i):
        obj = objects[i]
        obj = sc.rotate((0, 0, tilt_angle))(obj)
        obj = sc.rotate((90, 0, 0))(obj)
        facing_angle = math.degrees(i * hstep / radius)
        obj = sc.rotate(facing_angle + 90)(obj)
        hpos = utils.unit_point2(facing_angle) * radius
        pos = (*hpos, i * vstep)
        obj = sc.translate(pos)(obj)
        return obj

    return sc.union()([create(i) for i in range(len(objects))])


def create_tube(text):
    def create(char):
        return sc.linear_extrude(0.1)(sc.text(char, size=1, font="Monaco", segments=100))

    objects = [create(char) for char in text]
    wrap = wrap_tube(objects, 10, 0.7, 0.02)
    wrap = sc.translate((0, 0, 0.5))(wrap)
    return wrap


text = "I met a traveller from an antique land, Who said — Two vast and trunkless legs of stone Stand in the desert. . . . Near them, on the sand, Half sunk a shattered visage lies, whose frown, And wrinkled lip, and sneer of cold command, Tell that its sculptor well those passions read Which yet survive, stamped on these lifeless things, The hand that mocked them, and the heart that fed; And on the pedestal, these words appear: My name is Ozymandias, King of Kings; Look on my Works, ye Mighty, and despair! Nothing beside remains. Round the decay Of that colossal Wreck, boundless and bare The lone and level sands stretch far away."


def create_cup():
    height = 27.5
    cup = sc.cylinder(10, height, center=True, segments=200)
    cup = sc.translate((0, 0, height / 2))(cup)
    cutter = sc.cylinder(9.5, height, center=True, segments=200)
    cutter = sc.translate((0, 0, 1 + height / 2))(cutter)
    cup = cup - cutter
    return cup


tube = create_tube(text + " " + text)
cup = create_cup()

d = sc.color("gold")(tube) + sc.color("blue")(cup)
sc.scad_render_to_file(d, "/tmp/output.scad")
