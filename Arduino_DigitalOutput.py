import serial
import time

class digout():
    def __init__(self,comm_port):
        self.comm = serial.Serial(port=comm_port)

        self.settings = self.comm.get_settings()


    def send_command(self,command):
        self.comm.write(command.encode())


if __name__ == '__main__':
    pump_switches = digout(comm_port='COM10')

    try:
        while True:
            pump_switches.send_command('1000\n')
            print('Pump 1 On')

            time.sleep(1)

            pump_switches.send_command('0000\n')
            print('Pump 1 Off')

            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping')