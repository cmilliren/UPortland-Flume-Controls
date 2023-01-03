
class sed_flux_control():
    def __init__(self,dump_weight):
        self.dump_weight = dump_weight #lbs

    def update(self,do_obj,sct_obj):
        sct_obj.read_weights()

        if sct_obj.net_weight > self.dump_weight:
            do_obj.dump_sed()


if __name__ == '__main__':

    import Arduino_DigitalOutput as arduino
    import SCT1100_ASCII_funcs as sct1100
    import time

    do = arduino.digout('COM14')
    sct = sct1100.SCT1100('COM5')
    
    sedflux = sed_flux_control(1)

    try:
        while True:
            sedflux.update(do_obj=do,sct_obj=sct)
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping')


