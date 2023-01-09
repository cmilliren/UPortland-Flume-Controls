import minimalmodbus

class badger_flowmeter():
    def __init__(self,comm_port,slave_id):
        try: 
            self.comm = minimalmodbus.Instrument(comm_port, slave_id, debug=False) # port name, slave address (in decimal)
            self.comm.serial.baudrate = 9600 # Baud
            self.comm.serial.bytesize = 8
            self.comm.serial.parity = 'E'
            self.comm.serial.stopbits = 1
            self.comm.serial.timeout = 0.1  # seconds
            self.comm.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
            self.status  = 'Com Port Found: '+comm_port
        except Exception as e:
            print('Error Opening Com port for Badger Flowmeter:  '+str(e))
            # print(e)
            self.status = 'Com Port Not Found: '+comm_port

        self.comm_errors = 0
        self.flowrate = float('nan')

    def read_flowrate(self):
        try:
            self.flowrate = self.comm.read_float(registeraddress=int('ED',16),functioncode=3) # m3/s

        except Exception as e:
            print('Error Reading Badger Flowmeter: '+str(e))
            # print(e)
            self.flowrate = float('nan')

            self.comm_errors += 1



if __name__ == '__main__':
    flowmeter = badger_flowmeter('COM5',1)
    print(flowmeter.status)

    flowmeter.read_flowrate()

    print(flowmeter.flowrate)