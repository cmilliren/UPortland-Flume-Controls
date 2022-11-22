import minimalmodbus
import numpy as np

class adam4024():
    def __init__(self,comm_port,slave_id):
        try: 
            self.comm = minimalmodbus.Instrument(comm_port, slave_id, debug=False) # port name, slave address (in decimal)
            self.comm.serial.baudrate = 9600  # Baud
            self.comm.serial.bytesize = 8
            self.comm.serial.parity = 'N'
            self.comm.serial.stopbits = 1
            self.comm.serial.timeout = 1   # seconds
            self.comm.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
            self.status  = 'VFD Com Port Found: '+comm_port
        except Exception as e:
            print(e)
            self.status = 'VFD Com Port Not Found: '+comm_port

        self.comm_errors = 0
        self.analog_input = [float('nan'),float('nan')]

    def set_volts(self,channel,volts):
        bits = np.interp(volts,[-10,10],[0,4095])
        self.comm.write_register(channel,bits)

    def read_setpoint(self,channel):
        response = self.comm.read_register(channel,0)
        volts = np.interp(response,[0,4095],[-10,10])
        return volts

if __name__ == '__main__':
    ao = adam4024(comm_port='COM10',slave_id=1)
    ao.set_volts(channel=1,volts=-2.25)
    setpoint = ao.read_setpoint(channel=0)
    print(setpoint)

    