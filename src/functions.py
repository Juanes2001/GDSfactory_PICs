import gdsfactory  as gf
from pyglet.libs.win32 import com


def create_component():
    c = gf.Component()
    return c

def add_component(layout, component):
    com_ref = layout << component
    return  com_ref

def taper(length, width1, width2, style):
    c = gf.components.taper(length=length, width1=width1, width2=width2, cross_section=style)
    # el cross section es la forma
    # que adopta la seccion transversal, en este caso es cuadrado
    c.draw_ports()
    c.pprint_ports()
    c.show()


