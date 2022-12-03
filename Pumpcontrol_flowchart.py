import schemdraw
from schemdraw import flow


with schemdraw.Drawing(backend='svg') as d:
    d.config(fontsize=10, unit=1.5)
    d += flow.Terminal().label('DAQ Computer').drop('E')
    d += flow.Arrow().label('USB')
    d += flow.Box().label('FTDI COM4')
    d += flow.Arrow().label('RS485\nModbus')
    d += flow.Box().label('ADAM 4024 AO')
    d += flow.Arrow().label('0-10VDC')
    d += flow.Ellipse().label('Lenze VFD')

