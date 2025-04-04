import gdsfactory  as gf

def taper(length, width1, width2, style):
    c = gf.components.taper(length=length, width1=width1, width2=width2, cross_section=style)
    # el cross section es la forma
    # que adopta la seccion transversal, en este caso es cuadrado
    c.draw_ports()
    c.pprint_ports()
    c.show()
