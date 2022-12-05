# University of Portland Flume


## Lenze VFDs
### Control Overview
![alt text](https://github.umn.edu/safl-engineering/UPortland/blob/main/Pumpcontrol_flowchart.svg)

### Analog Input Speed Control
The fill, empty, auger and eductor pumps don't have Modbus so are controlled with analog inputs from the ADAM-4024 in the main enclosure. Below are the settings required in the VFD to enable control over analog input

| Parameter Number          | Name                                  | Setting           |
|---------------------------|---------------------------------------|-------------------|
| P201.01                   | Frequency setpoint Source             | 2: Analog Input 1 |
| P430.01                   | Analog input 1: Input range           | 2: 2 to 10 V    |
| P430.02                   | Analog input 1: Min frequency value   | 0.0 Hz            |
| P430.03                   | Analog input 1: Max frequency value   | 60.0 Hz           |
| P430.06                   | Analog input 1: Filter time           | 10 ms             |
| P400.12                   | Run Command Source                    | Digital Input 1   |
| P200.00                   | Control Select                        | 0: Flexible IO    |

### Control Wiring for VFDs

| Purpose                   |    VFD Terminal                       | DAQ Enclosure         |
|---------------------------|---------------------------------------|-----------------------|
| Freq Setting Voltage      | AI 1                                  | ADAM-4020 VOUT x      |
| Freq Setting G            | G                                     | ADAM-4020 G           |
| Run Command               | DI 1                                  | Crydom SSR Terminal 2 |
| E-Stop                    |                                       |                       |

Run Command Relay Wiring: 
| Purpose                   | Source                                | Relay Connection      |
|---------------------------|---------------------------------------|-----------------------|
| Run Command 24V           |  DAQ Enclosure 24VDC terminal blocks  | Crydom SSR Terminal 1 |
| Relay Switching Signal    |  Arduino Pin 9, 10, 11, 12            | Crydom SSR Terminal 3 |
| Relay Switching Signal G  |  Arduino Pin G                        | Crydom SSR Terminal 4 |

### Modbus Control of 25HP Lenze VFD

Dip Switches: 
1 = ON
b = ON
a = ON 
all others off

You need to have a jumper between 24V and DI1 on the X3 terminals in order for the pump to start with modbus commands. 

| Parameter Number          | Name                                  | Setting           |
|---------------------------|---------------------------------------|-------------------|
| P510.02                   | Baud Rate                             | 5: 38400          |
| P510.03                   | Data Format                           | 4: 8,N,1          |
| P400.37                   | Network Control                       | 1: True           |
| P201.01                   | Freq Setpoint Source                  | 5: Network        |
| P400.01                   | Run Control Source                    | 11: Digital Input 1|
