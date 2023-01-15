import minimalmodbus
import dummy_serial as dummy

class lenze_vfd():
    def __init__(self,comm_port,slave_id):
        try: 
            self.comm = minimalmodbus.Instrument(comm_port, slave_id, debug=False) # port name, slave address (in decimal)
            self.comm.serial.baudrate = 38400 # Baud
            self.comm.serial.bytesize = 8
            self.comm.serial.parity = 'N'
            self.comm.serial.stopbits = 1
            self.comm.serial.timeout = 0.1   # seconds
            self.comm.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
            # self.status  = 'VFD Com Port Found: '+comm_port
        except Exception as e:
            print(e)
            self.comm = dummy.dummy_modbus()

        self.comm_errors = 0
        self.status = {'Comms OK': False,
                     'Fault':False,
                     'Warning':False,
                     'RunningForward':False,
                     'RunningRev':False,
                     'Ready':False,
                     'NetworkControlActive':False,
                     'NetowrkSetpointActive':False,
                     'AtReference':False,
                     'ProfileStateBit0':False,
                     'ProfileStateBit1':False,
                     'ProfileStateBit2':False,
                     'ProfileStateBit3':False,
                     'ProcesscontrollerActive':False,
                     'TorqueModeActive':False,
                     'CurrentLimitReached':False,
                     'DCBrakingActive':False
                     }

    def read_setpoint(self):
        try: 
            self.current_setpoint = self.comm.read_register(2101,0,3)
        except Exception as e:
            print(e)
            self.current_setpoint = float('nan')
            self.comm_errors += 1

    def send_setpoint(self,freq):
        try: 
            self.comm.write_register(2101,freq,2)

        except Exception as e:
            print(e)
            self.comm_errors +=1

    def start_pump(self):
        try:
            self.comm.write_register(2100,int(b'0000000001100001',2),0)
        except Exception as e:
            self.comm_errors = self.comm_errors + 1
            print(e)

    def stop_pump(self):
        try:
            self.comm.write_register(2100,int(b'0000000000000000',2),0)
        except Exception as e:
            self.comm_errors = self.comm_errors + 1
            print(e)
    def reset_fault(self):
        try:
            self.comm.write_register(2106,int(b'0000000010000000',2),0)
            # self.comm.write_register(2106,int(b'0000000000000000',2),0)
        except Exception as e:
            print(e)


    def poll_status(self):
        try:
            self.read_setpoint()
            status_bin= self.comm.read_register(2000,0)
            status_bin = format(status_bin,'016b')

            i = -1
            for n in self.status:
                self.status[n] = bool(int(status_bin[i]))
                i = i-1

            self.status[0] = True

        except Exception as e:
            print(e)
            # self.status = float('nan')
            self.status[0] = False
            self.comm_errors += 1



if __name__ == '__main__':

    import time

    vfd= lenze_vfd(comm_port='COM5',slave_id=1)

    vfd.poll_status
    vfd.send_setpoint(11.11)
    vfd.reset_fault()
    time.sleep(1)
    vfd.start_pump()

    try: 
        while True: 
            vfd.poll_status()
            print('Fault: '+str(vfd.status['Fault']))
            print('Running Forward: '+str(vfd.status['RunningForward']))
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping')
        vfd.stop_pump()
