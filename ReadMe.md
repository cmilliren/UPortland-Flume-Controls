# University of Portland Flume

## Lenze VFD Settings
List of changed parameters for Lenze VFDs

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