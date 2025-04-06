import gdsfactory  as gf
from pyglet.libs.win32 import com


def create_component():
    c = gf.Component()
    return c

def taper(length, width1, width2, crss_section):
    c = gf.components.taper(length=length, width1=width1, width2=width2, cross_section=crss_section)
    # el cross section es la forma
    # que adopta la seccion transversal, en este caso es cuadrado
    return c

def str_line(length, num_points, crss_section):
    # Import the structure
    c = gf.components.straight(length=length, npoints=num_points, cross_section=crss_section)
    return c





