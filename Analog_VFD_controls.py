import ADAM_4024_AnalogOut as adam
import Arduino_DigitalOutput as arduino

ao = adam.adam4024('COM15',1)
do = arduino.digout('COM14')

class vfd():
    def __init__(self,channel_num):
        self.channel = channel_num
        self.ao = ao
        self.do = do

    def set_freq(self,freq):
        self.ao.set_freq(channel=self.channel,freq=freq)

    def start_vfd(self):
        self.do.start(self.channel)

    def stop_vfd(self):
        self.do.stop(self.channel)


if __name__ == '__main__':
    fill_pump = vfd(0)
    fill_pump.set_freq(50)
    fill_pump.start_vfd()



