import gdsfactory  as gf

# Import the structure
c = gf.components.straight(length=10, npoints=2, cross_section='rib')
c.draw_ports()
c.pprint_ports()
c.plot()
c.show()