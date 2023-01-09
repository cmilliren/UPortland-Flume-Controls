import serial
import dummy_serial as dummy

class SCT1100():
    def __init__(self,comm_port):
        try:
            self.comm = serial.Serial(port=comm_port,baudrate=38400,bytesize=8,parity='N',stopbits=1,timeout=1)
            
        except Exception as e:
            print(e)
            self.comm = dummy.dummy_port(comm_port=comm_port)

        self.comm_errors = 0


    def read_weights(self):
        scale_status_dict  = {'ST':'Stable','US':'Unstable','UL':'Under Load','OL':'Overload'}    

        try:
            command = 'REXT'+chr(13)+chr(10)
            # print(f'Command: {command.encode()}')
            self.comm.write(command.encode())
            response = self.comm.read_until('\n')
            # print(f'Response: {response}')

            response = response.decode('utf-8').strip().replace(' ','')
            values = response.split(',')
            
            if len(values) < 6:
                raise Exception ('Error received from SCT-1100')

            self.scale_status = scale_status_dict[values[1]]
            self.net_weight   = float(values[2])
            self.tare_weight  = float(values[3])
            self.units        = values[5]

        except Exception as e:
            print(e)
            self.scale_status = 'nan'
            self.net_weight   = float('nan')
            self.tare_weight  = float('nan')
            self.units        = 'nan'
            self.comm_errors += 1

    def read_net(self):
        try:
            self.net = self.comm.read_register(registeraddress=1101,functioncode=3,number_of_decimals=2)
        except Exception as e:
            print(e)
            self.net = float('nan')

    def tare(self):
        try: 
            command = 'TARE'+chr(13)+chr(10)
            self.comm.write(command.encode())

            response = self.comm.read_until('\n')
            print(response)

        except Exception as e:
            print(e)

    def read_software_version(self):
        try:
            command = 'VER'+chr(13)+chr(10)
            print(f'Command: {command.encode()}')
            self.comm.write(command.encode())
            self.version = self.comm.read_until('\n')

        except Exception as e:
            print(e)
            self.version = float('nan')


if __name__ == '__main__':
    import time


    sct = SCT1100('COM5')


    try:
        while True:
            sct.read_weights()
            
            print(f'Scale Status : {sct.scale_status}')
            print(f'Net Weight : {sct.net_weight}')
            print(f'Tare Weight : {sct.tare_weight}')
            print(f'Units: {sct.units}')


            time.sleep(0.5)

    except KeyboardInterrupt:
        print('Stopping')