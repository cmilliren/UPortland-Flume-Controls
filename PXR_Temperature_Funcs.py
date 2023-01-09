import minimalmodbus
import dummy_serial as dummy

class pxr():
    def __init__(self,comm_port,slave_id):
        try:
            self.comm = minimalmodbus.Instrument(comm_port,slave_id)
            self.comm.serial.baudrate = 9600
            self.comm.serial.bytesize = 8
            self.comm.serial.parity = 'O'
            self.comm.serial.stopbits = 1
            self.comm.serial.timeout = 0.1
            self.comm.mode = minimalmodbus.MODE_RTU='rtu'
        except Exception as e:
            print(e)
            self.comm = dummy.dummy_modbus()


        self.temperature = float('nan')

    def read_temperature(self):
        
        try: 
            temperature = self.comm.read_register(1000,1,4)
            if temperature > 100:
                temperature = float('nan')
        except Exception as e:
            print(e)
            temperature = float('nan')


        self.temperature = temperature

if __name__ == '__main__':
    import time

    temp = pxr('COM6',1)

    try: 
        while True:

            temp.read_temperature()
            time.sleep(0.5)

            print(f'PXR Tempertuare: {temp.temperature} degC')
    except KeyboardInterrupt:
        print('Stopping')