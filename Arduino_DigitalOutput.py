import serial
import dummy_serial as dummy

class digout():
    def __init__(self,comm_port):
        try:
            self.comm = serial.Serial(port=comm_port,timeout=10)

            self.settings = self.comm.get_settings()

        except Exception as e:
            print(e)
            self.comm = dummy.dummy_port(comm_port=comm_port)

        self.command = '00000'
        self.start_bit_array = ['0','0','0','0','0','0']


    def start(self,array_idx):
        self.start_bit_array[array_idx] = '1'
        self.command = ''.join(self.start_bit_array)
        self.send_command()
    
    def stop(self,array_idx):
        self.start_bit_array[array_idx] = '0'
        self.command = ''.join(self.start_bit_array)
        self.send_command()


    def send_command(self):
        # self.comm.flush()
        # print(self.command)
        self.comm.write(self.command.encode())
        # time.sleep(0.1)
        self.comm.flush()
        self.response = self.comm.read_until(b'>').decode('utf-8').strip()


if __name__ == '__main__':
    pump_switches = digout(comm_port='COM14')

    pump_switches.start_fill_pump()

    # try:
    #     while True:
    #         command = input('Enter Pump Command (e.g. 10001): ')

    #         pump_switches.send_command(command)

    #         print(pump_switches.response)

    # except KeyboardInterrupt:
    #     print('Stopping')