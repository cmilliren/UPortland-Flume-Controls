
class sed_flux_control():
    def __init__(self,do_obj):
        self.do = do_obj

if __name__ == '__main__':

    import ADAM_4024_AnalogOut as adam
    import Arduino_DigitalOutput as arduino

    ao = adam.adam4024('COM15',1)
    do = arduino.digout('COM14')
    fill_pump = vfd(0,ao,do)
    fill_pump.set_freq(50)
    fill_pump.start_vfd()



