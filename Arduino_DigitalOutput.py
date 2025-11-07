import serial
import dummy_serial as dummy
import time

class digout():
    def __init__(self,comm_port):
        try:
            self.comm = serial.Serial(port=comm_port,timeout=0.1,baudrate=115200)

            self.settings = self.comm.get_settings()

        except Exception as e:
            print(f'Error connecting to Arduino: {e}')
            print("Using a Dummy Serial Port for Arduino Coms")
            self.comm = dummy.dummy_port(verbose=False)


        self.start_bit_array = ['0','0','0','0','2']
        self.status = ''.join(self.start_bit_array)
        self.command = ''.join(self.start_bit_array)+'\n'
        self.send_command()

        self.fill_pump_enabled = False
        self.empty_pump_enabled = False
        self.sed_auger_enabled = False
        self.eductor_pump_enabled = False
        self.teknic_motor_enabled = False


    def start(self,array_idx):
        self.start_bit_array[array_idx] = '1'
        self.command = ''.join(self.start_bit_array)+'\n'
        self.send_command()
    
    def stop(self,array_idx):
        self.start_bit_array[array_idx] = '0'
        self.command = ''.join(self.start_bit_array)+'\n'
        self.send_command()

    def dump_sed(self):
        self.start_bit_array[-1] = '1'
        self.command = ''.join(self.start_bit_array)+'\n'
        self.send_command()
        
        # Set the bit back to low (no need to send it though)
        self.start_bit_array[-1] = '0'
        self.command = ''.join(self.start_bit_array)+'\n'

    def disable_teknic_motor(self):
        self.start_bit_array[-1] = '2'
        self.command = ''.join(self.start_bit_array)+'\n'
        self.send_command()

    def enable_teknic_motor(self):
        self.start_bit_array[-1] = '0'
        self.command = ''.join(self.start_bit_array)+'\n'
        self.send_command()

    def poll_status(self):
        self.comm.write('p\n'.encode())
        self.status = self.comm.read_until(b'>').decode('utf-8').strip()

        if self.status[0]=='1':
            self.fill_pump_enabled = 'Running'
        else:
            self.fill_pump_enabled = 'Stopped'

        if self.status[1] == '1':
            self.empty_pump_enabled = 'Running'
        else:
            self.empty_pump_enabled = 'Stopped'

        if self.status[2] == '1':
            self.sed_auger_enabled = 'Running'
        else: 
            self.sed_auger_enabled = 'Stopped'
        if self.status[3] == '1':
            self.eductor_pump_enabled = 'Running'
        else:
            self.eductor_pump_enabled = 'Stopped'

        if self.status[4] == '0':
            self.teknic_motor_enabled = 'Enabled'
        elif self.status[4] == '2':
            self.teknic_motor_enabled = 'Disabled'
        elif self.status[4] == '1':
            self.teknic_motor_enabled = 'Dumping'

    def send_command(self):
        self.comm.write(self.command.encode())
        # self.comm.flush()
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