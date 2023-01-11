class dummy_port():
    def __init__(self,comm_port):
        self.comm_port = comm_port
    def write(self,command):
        print(command)

    def read_until(self,terminator):
        print(f'Dummy SerialPort Response. with terminator {terminator}')

        return b'Dummy Response'

    def flush(self):
        pass

class dummy_modbus():
    def __init__(self):
        self.baudrate = 9600

    def write_register(self,register,value):
        print(f'Dummy Modbus Write to register: {register} \t value: {value}')

    def read_register(self,register,value1):
        print(f'Dummy Modbus read register: {register} \t value1: {value1} ')
        raise Exception