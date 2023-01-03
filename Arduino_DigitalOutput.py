import serial
import dummy_serial as dummy
import time

class digout():
    def __init__(self,comm_port):
        try:
            self.comm = serial.Serial(port=comm_port,timeout=10)

            self.settings = self.comm.get_settings()

        except Exception as e:
            print(e)
            self.comm = dummy.dummy_port(comm_port=comm_port)

        self.command = '00000'
        self.start_bit_array = ['0','0','0','0','0']
        self.send_command()


    def start(self,array_idx):
        self.start_bit_array[array_idx] = '1'
        self.command = ''.join(self.start_bit_array)
        self.send_command()
    
    def stop(self,array_idx):
        self.start_bit_array[array_idx] = '0'
        self.command = ''.join(self.start_bit_array)
        self.send_command()

    def dump_sed(self):
        self.start_bit_array[-1] = '1'
        self.command = ''.join(self.start_bit_array)
        self.send_command()
        
        # Set the bit back to low (no need to send it though)
        self.start_bit_array[-1] = '0'
        self.command = ''.join(self.start_bit_array)

    def send_command(self):
        # self.comm.flush()
        # print(self.command)
        self.comm.write(self.command.encode())
        # time.sleep(0.1)
        self.comm.flush()
        self.response = self.comm.read_until(b'>').decode('utf-8').strip()


if __name__ == '__main__':
    # pump_switches = digout(comm_port='COM14')

    # pump_switches.start_fill_pump()
    
    dig_out = digout(comm_port='COM14')


    try:
        while True:
            print('Triggering Sed dump')
            dig_out.dump_sed()
            print(f'Response from Arduino: {dig_out.response}')
            time.sleep(10)

    except KeyboardInterrupt:
        print('Stopping')