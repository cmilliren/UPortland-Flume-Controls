
class sed_flux_control():
    def __init__(self,default_weight,do,sct_obj):
        self.sct = sct_obj
        self.do = do
        self.dump_weight = float(default_weight) #lbs

    def update(self):
        self.sct.read_weights()

        if self.sct.net_weight > self.dump_weight:
            self.do.dump_sed()

    def set_dump_weight(self,dump_weight):
        self.dump_weight = dump_weight


if __name__ == '__main__':

    import Arduino_DigitalOutput as arduino
    import SCT1100_ASCII_funcs as sct1100
    import time

    do = arduino.digout('COM14')
    sct = sct1100.SCT1100('COM5')
    
    sedflux = sed_flux_control(1,do,sct)

    try:
        while True:
            sedflux.update()
            print(sedflux.sct.net_weight)
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping')


