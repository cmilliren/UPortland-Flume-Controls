import serial
import struct


class massa():
    def __init__(self,comm_port,ids):
        self.ids = ids # array of massa id numbers

        try:
            self.comm = serial.Serial(comm_port,baudrate=19200,timeout=1,bytesize=8,parity='N',stopbits=1)
        except Exception as e:
            print(f'Unable to open Massa Com Port: {comm_port}')
            print(e)



    def poll_status(self):

        self.massa_id_array = []
        self.error_array    = []
        self.dist_cm_array  = []
        self.target_array   = []
        self.strength_array = []
        self.massa_temperature_array = []


        for i in range(len(self.ids)):
            # print(f'Polling Massa with ID: {self.ids[i]}')
            # Format the message to request the status from the Massa
            message=[170, int(self.ids[i]), 3, 0, 0, (170+int(self.ids[i])+3+0+0) % 256]
            b=bytes(message)

            # Send the message and read the response
            try:
                # print(i)
                self.comm.write(b)
                # self.comm.flush()
                res=self.comm.read(6)

                # print(res)
                # Parse the response
                massa_id=res[0]  # Massa ID number

                dist_data=bytearray([res[2], res[3]])  # Massa Distance in two Bytes
                dist_int=struct.unpack(
                    '<H', dist_data)  # Conver the distance to an unsigned int\
                dist=dist_int[0]/128  # Convert from unsigned int to distance in inches
                dist_cm=dist*2.54  # Convert from inches to cm
                # print(f'Distance Measurement for Massa with ID={self.ids[i]} :{dist_cm:.2f} cm')

                # Internal temperature of the Massa
                massa_temperature=res[4]*0.48876-50

                # Parse Diagnostics
                diag='{0:08b}'.format(res[1])
                err=diag[7]
                error_key={'0': 'OK', '1': 'Error'}
                error=error_key[err]

                target_detected=diag[4]
                target_detected_key={'0': 'No', '1': 'Yes'}
                target=target_detected_key[target_detected]

                strength_binary=diag[0:4]
                strength_key={'0000': '0%', '0001': '25%',
                    '0010': '50%', '0011': '75%', '0100': '100%'}
                strength = strength_key[strength_binary]

                # Validate Massa Measurements
                if target_detected == '0':
                    dist_cm = float('nan')

                ## Add measurements to arrays
                
                self.massa_id_array.append(massa_id)
                self.error_array.append(error)
                self.dist_cm_array.append(dist_cm)
                self.target_array.append(target)
                self.strength_array.append(strength)
                self.massa_temperature_array.append(massa_temperature)
            
            except Exception as e:
                raise(e)
                print(e)
            
            



if __name__ == '__main__':
    import time
    
    massas = massa('COM7',ids=[1,2])

    try:
        while True:
                    
            massas.poll_status()

            print(f'Massa Distance Array: {massas.dist_cm_array}')

            # print(f'Distance: {massa_1.dist_cm[0]} cm')
            # print(f'Target Detected: {massa_1.target[0]}')
            # print(f'Massa Temperature: {massa_1.massa_temperature[0]} degC')
            # print(f'Signal Strength: {massa_1.strength[0]}\n\n')

            time.sleep(0.5)
    except KeyboardInterrupt:
        print('Stopping')
