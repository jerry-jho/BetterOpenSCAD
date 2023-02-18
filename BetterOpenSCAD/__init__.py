from solid.utils import up, down, forward, back, right, left
from solid import cylinder, cube, scad_render, translate, rotate
from solid import linear_extrude, text
import tempfile
import os
import subprocess


def T(x, y=0, z=0):
    if isinstance(x, (list, tuple)):
        x, y, z = x
    return translate([x, y, z])


def R(x, y=0, z=0):
    if isinstance(x, (list, tuple)):
        x, y, z = x
    return rotate([x, y, z])


def DRILL(x: float, y: float, r: float):

    H = 1000
    return down(100)(forward(y)(right(x)(cylinder(r, H, segments=180))))


def X(t):
    if t > 0:
        return right(t)
    else:
        return left(t)


def Y(t):
    if t > 0:
        return forward(t)
    else:
        return back(t)


def Z(t):
    if t > 0:
        return up(t)
    else:
        return down(t)


def CUBE(w, h=None, d=None, x=0, y=0, z=0):
    if isinstance(w, (list, tuple)):
        w, h, d = w
    else:
        if h is None:
            h = w
        if d is None:
            d = w
    return translate([x, y, z])(cube([w, h, d]))


def CYLINDER(r, h, x=0, y=0, z=0):
    return translate([x, y, z])(cylinder(r, h, segments=180))


def TEXT(t, s, x=0, y=0, z=0):
    return translate([x, y, z])(linear_extrude(height=s, convexity=4)()(text(
        t,
        size=s * 22 / 30,
        font="Bitstream Vera Sans",
        halign="center",
        valign="center")))


def RENDER(obj, output=None):
    v = scad_render(obj)
    if output is not None:
        if output.endswith('.scad'):
            with open(output, 'w') as fp:
                fp.write(v)
        elif output.endswith('.stl'):
            try:
                os.unlink(output)
            except Exception:
                pass
            fp = tempfile.NamedTemporaryFile(delete=False)
            fp.write(v.encode(encoding='UTF-8'))
            name = fp.name
            fp.close()
            subprocess.run(['openscad', '-o', output, name])
            os.unlink(name)
            print("Output:", output)
    else:
        print(v)
