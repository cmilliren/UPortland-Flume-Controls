class dummy_port():
    def __init__(self,verbose):
        self.verbose = verbose
    def write(self,command):
        if self.verbose:
            print(command)

    def read_until(self,terminator):
        if self.verbose: 
            print(f'Dummy SerialPort Response. with terminator {terminator}')

        return b'Dummy Response'
    
    def read(self,num_bytes):
        return bytes(num_bytes)

    def flush(self):
        pass

class dummy_modbus():
    def __init__(self,verbose):
        self.verbose = verbose

    def write_register(self,register,value,decimals):
        if self.verbose:
            print(f'Dummy Modbus Write to register: {register} \t value: {value} \t decimals: {decimals}')

    def read_register(self,register,*args):
        if self.verbose:
            print(f'Dummy Modbus read register: {register}')
        return 0
        # raise Exception