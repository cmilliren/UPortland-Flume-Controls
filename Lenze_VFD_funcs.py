import minimalmodbus
import dummy_serial as dummy
import json

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
            self.comm = dummy.dummy_modbus(verbose=False)

        self.comm_errors = 0
        self.comm_OK = False
        self.status = {'Fault':False,
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
        self.error_code = float('nan')
        self.error_message = 'Error polling VFD error code'

        # Read the list of error code descriptions from json file:
        with open('lenze_errors.json') as fid:
            self.error_desc = json.load(fid)

    def read_setpoint(self):
        try: 
            self.current_setpoint = self.comm.read_register(registeraddress=2101,number_of_decimals=2,functioncode=3)
            self.comm_OK = True
        except Exception as e:
            # print(f'Lenze Modbus Comm Error: {e}')
            self.current_setpoint = float('nan')
            self.comm_errors += 1
            self.comm_OK = False

    def send_setpoint(self,freq):
        try: 
            self.comm.write_register(2101,freq,2)
            self.comm_OK = True

        except Exception as e:
            print(e)
            self.comm_errors +=1
            self.comm_OK = False

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

    def read_error_code(self):
        try:
            self.error_code = self.comm.read_register(registeraddress=2002,number_of_decimals=0,functioncode=3)
            self.error_message = self.error_desc[str(self.error_code)]['Error message']                        
            
            
            self.comm_OK = True

        except Exception as e:
            # print(f'Lenze- Error polling error code: {e}')
            self.comm_OK = False


    def poll_status(self):
        try:
            self.read_setpoint()
            self.read_error_code()

            status_bin= self.comm.read_register(2000,0)
            status_bin = format(status_bin,'016b')
        except Exception as e:
            # print(f'Lenze Modbus Comm Error: {e}')
            status_bin = format(0,'016b')
            self.comm_OK = False
            self.comm_errors += 1

        try:           

            i = -1
            for n in self.status:
                # print(f'i value : {i}')
                # print(f'status entry: {n}')
                self.status[n] = bool(int(status_bin[i]))
                i = i-1


        except Exception as e:
            # raise e
            print(f'Lenze VFD  Error Parsing status word: {e}')
            self.status['Comms OK'] = False
            



if __name__ == '__main__':

    import time

    vfd= lenze_vfd(comm_port='COM3',slave_id=1)

    vfd.poll_status
    vfd.send_setpoint(5)
    vfd.reset_fault()
    time.sleep(1)
    # vfd.start_pump()

    try: 
        while True: 
            vfd.poll_status()
            vfd.read_error_code()

            print('Comms OK: '+str(vfd.comm_OK))
            print('Fault: '+str(vfd.status['Fault']))
            print('Running Forward: '+str(vfd.status['RunningForward']))
            print(f'Setpoint: {vfd.current_setpoint:.2f} Hz')
            print(f'Error Code: {vfd.error_code}')
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping')
        vfd.stop_pump()
