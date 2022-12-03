import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d: 
    d += (Vin:=elm.Line().label('24VDC Input'))
    d += elm.Dot()
    d += (r1:=elm.Resistor().label('10k'))
    d += elm.Dot()
    d += (r2:=elm.Resistor().label('12k').at(r1.end))
    d += elm.Ground()
    d += elm.Line().down().at(r1.end).label('10VDC')

    d += elm.Line().up().at(r1.start)
    d += elm.Line().right()
    d += elm.SwitchDpdt()