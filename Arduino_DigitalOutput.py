import serial
import time

class digout():
    def __init__(self,comm_port):
        self.comm = serial.Serial(port=comm_port,timeout=10)

        self.settings = self.comm.get_settings()
        self.command = '00000'

    def start_fill_pump(self):
        self.command[0] = '1'
        self.send_command()
    
    def stop_fill_pump(self):
        self.command[0] = '0'
        self.send_command()


    def send_command(self):
        # self.comm.flush()
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