from solid.utils import up, down, forward, back, right, left
from solid import cylinder, cube, scad_render, translate, rotate
from solid import linear_extrude, text
import tempfile
import os
import subprocess

g_segments = int(os.getenv('SCAD_SEGMENT', 180))


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
    return down(100)(forward(y)(right(x)(cylinder(r, H, segments=g_segments))))


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
    return translate([x, y, z])(cylinder(r, h, segments=g_segments))


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
            print("Segments: ", g_segments)
            fp = tempfile.NamedTemporaryFile(delete=False)
            fp.write(v.encode(encoding='UTF-8'))
            name = fp.name
            fp.close()
            subprocess.run(['openscad', '-o', output, name])
            os.unlink(name)
            print("Output:", output)
    else:
        print(v)


def STL2OBJ(stl_file, obj_file):
    from stl import mesh
    import math
    m = mesh.Mesh.from_file(stl_file)
    m.rotate([0.5, 0.0, 0.0], math.radians(90))

    vectors = m.vectors
    normals = m.normals
    vectors_key_list = []
    vectors_list = []
    normals_key_list = []
    normals_list = []
    triangle_list = []
    for i, vector in enumerate(vectors):
        one_triangle = []
        for j in range(3):
            v_key = ",".join(map(str, vectors[i][j][:3]))
            if v_key in vectors_key_list:
                v_index = vectors_key_list.index(v_key)
            else:
                v_index = len(vectors_key_list)
                vectors_key_list.append(v_key)
                vectors_list.append(vectors[i][j][:3])
            one_triangle.append(v_index + 1)

        n_key = ",".join(map(str, normals[i][:3]))
        if n_key in normals_key_list:
            n_index = normals_key_list.index(n_key)
        else:
            n_index = len(normals_key_list)
            normals_key_list.append(n_key)
            normals_list.append(normals[i][:3])

        # print(normals_list)
        triangle_list.append((one_triangle, n_index + 1))

    with open(obj_file, "w") as fh:
        print("# {} {}".format(m.name, ''), file=fh)
        print("", file=fh)
        for v in vectors_list:
            print("v {} {} {}".format(v[0], v[1], v[2]), file=fh)
        for vn in normals_list:
            print("vn {} {} {}".format(vn[0], vn[1], vn[2]), file=fh)
        for t in triangle_list:
            faces = t[0]
            normal = t[1]

            print("f {}//{} {}//{} {}//{}".format(
                faces[0], normal,
                faces[1], normal,
                faces[2], normal,
            ), file=fh)
