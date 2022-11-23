import minimalmodbus
import numpy as np
import Arduino_DigitalOutput as on_off

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

    def set_freq(self,channel,freq):
        bits = np.interp(freq,[0,60],[2457,4095])
        self.comm.write_register(channel,bits)


    def read_setpoint(self,channel):
        response = self.comm.read_register(channel,0)
        freq = np.interp(response,[2457,4095],[0,60])
        return freq

if __name__ == '__main__':
    ao = adam4024(comm_port='COM5',slave_id=1)
    sw = on_off.digout(comm_port='COM10')

    current_setpoint = ao.read_setpoint(2)

    input(f'Current setpoint is {current_setpoint:.2f}. Press Enter to Start Pump.  Ctl-C to Stop')

    sw.send_command('1000')

    try:
        while True:
            # setpoint =input('Enter Voltage:')
            # ao.set_volts(channel=2,volts=setpoint)
            setpoint = input('Enter Freq (0 to 60):')
            ao.set_freq(channel=2,freq=setpoint)

            setpoint_current = ao.read_setpoint(channel=2)
            print(setpoint_current)
    except KeyboardInterrupt:
        print('Stopping.')
        sw.send_command('0000')

    