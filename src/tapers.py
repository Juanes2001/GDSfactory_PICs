import gdsfactory  as gf

# ---Definition of the Taper Parameters---#
taper_length = 300 # micras
wg_width_1 = 3 # micras
wg_width_2 = 0.8 # micras

#-- Import the Taper object from GDSFactory
c = gf.components.taper(length=taper_length, width1=wg_width_1, width2=wg_width_2, cross_section="strip")
# el cross section es la forma
# que adopta la seccion transversal, en este caso es cuadrado

c.draw_ports()
c.pprint_ports()
c.plot()
c.show() # abrir en klayout

