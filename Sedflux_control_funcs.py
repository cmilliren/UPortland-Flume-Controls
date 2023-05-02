import collections

class sed_flux_control():
    def __init__(self,default_weight,do,sct_obj,tare_weight):
        self.sct = sct_obj
        self.do = do
        self.dump_weight = float(default_weight) #lbs
        self.tare_weight = tare_weight

        self.FIFO_length = 20
        # self.update()
        self.FIFO = collections.deque([],self.FIFO_length)

    def update(self):
        self.sct.read_weights()
        self.sct.net_weight = self.sct.net_weight-self.tare_weight
        self.FIFO.append(self.sct.net_weight)
        self.moving_average = sum(self.FIFO)/len(self.FIFO)
        # print(f'Sed Weight Moving Average: {self.moving_average:.2f}')

        if self.sct.net_weight > self.dump_weight:
            self.do.dump_sed()

    def set_dump_weight(self,dump_weight):
        self.dump_weight = dump_weight

    def tare(self):
        # self.sct.read_weights()
        # self.tare_weight = self.sct.net_weight
        self.tare_weight = self.tare_weight + self.moving_average


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


