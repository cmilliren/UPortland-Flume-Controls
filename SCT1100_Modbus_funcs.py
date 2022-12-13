import minimalmodbus

class SCT1100():
    def __init__(self,comm_port,slave_id):
        self.comm = minimalmodbus.Instrument(comm_port,slave_id)
        self.comm.serial.baudrate = 38400
        self.comm.serial.bytesize = 8
        self.comm.serial.parity = 'N'
        self.comm.serial.stopbits = 1
        self.comm.serial.timeout = 1
        self.comm.mode = minimalmodbus.MODE_RTU='rtu'

        self.comm_errors = 0


    def read_weights(self):
        try:
            self.weights = self.comm.read_registers(registeraddress=1100,functioncode=3,number_of_registers=3)
            self.gross = self.weights[0]/100
            self.net   = self.weights[1]/100
            self.tare  = self.weights[2]/100
        except Exception as e:
            print(e)
            self.gross = float('nan')
            self.net = float('nan')
            self.tare = float('nan')
            self.comm_errors += 1

    def read_net(self):
        try:
            self.net = self.comm.read_register(registeraddress=1101,functioncode=3,number_of_decimals=2)
        except Exception as e:
            print(e)
            self.net = float('nan')

    def tare(self):
        try: 
            self.comm.write_register(registeraddress=230,value=3,number_of_decimals=0,functioncode=6)

        except Exception as e:
            print(e)

    def read_software_version(self):
        try:
            self.version = self.comm.read_registers(100,2,functioncode=4,)
        except Exception as e:
            print(e)
            self.version = float('nan')


if __name__ == '__main__':
    import time


    sct = SCT1100('COM5',1)

    print('Tare Scale')
    time.sleep(1)

    sct.tare()
    time.sleep(1)


    try:
        while True:
            sct.read_weights()

            print(f'Gross Weight: {sct.gross}')
            print(f'Net Weight: {sct.net}')
            print(f'Tare Weight: {sct.tare}')
            print(f'Cumulative Comm Errors: {sct.comm_errors}')
            print('---------------------------------')

            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping')