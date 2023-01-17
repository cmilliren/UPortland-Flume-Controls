# University of Portland Flume

## To Do:
- Integrate Massas into the GUI
- Wire Massas (Junction box?)
- Make cables for VFDs, Flowmeter, (others)
- buy ethernet and USB panel mount connectors for exterior of enclosure
- make relay for sed feed wash pump


## Lenze VFDs
![alt text](https://github.umn.edu/safl-engineering/UPortland/blob/main/Pumpcontrol_flowchart.svg)

### Analog Control 
#### Parameters for Analog Control VFDs
The fill, empty, auger and eductor pumps don't have Modbus so are controlled with analog inputs from the ADAM-4024 in the main enclosure. Below are the settings required in the VFD to enable control over analog input

| Parameter Number          | Name                                  | Setting               |
|---------------------------|---------------------------------------|-----------------------|
| P201.01                   | Frequency setpoint Source             | 2: Analog Input 1     |
| P430.01                   | Analog input 1: Input range           | 2: 2 to 10 V          |
| P430.02                   | Analog input 1: Min frequency value   | 0.0 Hz                |
| P430.03                   | Analog input 1: Max frequency value   | 60.0 Hz               |
| P430.06                   | Analog input 1: Filter time           | 10 ms                 |
| P400.12                   | Run Command Source                    | Digital Input 1       |
| P200.00                   | Control Select                        | 0: Flexible IO        |
| P411.02                   | Inversion of DI2                      | 1: Inverted           |
| P400.43                   | Function List: Activate Fault 1       | 12: Digital Input 2   |
| P420.01                   | Relay Control                         | 50: Running           |

* Note: P420.01 only needs to be set on the sed feed auger VFD.  This will activate the wash pump that sluices the sediment into the flume. 

#### Control Wiring for Analog Control VFDs

| Purpose                   |    Terminal 1                         | Terminal 2                          |
|---------------------------|---------------------------------------|-------------------------------------|
| Freq Setting Voltage      | AI 1  (Lenze `X3` Terminals)          | DAQ Enclosure ADAM-4020 VOUT x      |
| Freq Setting G            | G     (Lenze `X3` Terminals)          | DAQ Enclosure ADAM-4020 G           |
| Run Command               | DI 1  (Lenze `X3` Terminals)          | DAQ Enclosure Crydom SSR Terminal 2 |
| E-Stop                    | `24V` on Lenze `X3` Terminals         | `DI2` on Lenze `X3` Terminals       |
| Relay for Wash Pump  24V  | `COM` on Lenze `X9` Terminals         | DAQ Enclosure 24VDC                 |
| Realy for Wash Pump       | `NO`  on Lenze `X9` Terminals         | Wash Pump control box               |

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


### Rice Lake SCT-1100 Load Cell Transmitter

#### Changed Settings
| Parameter Name                |  New Setting                  |
|-------------------------------|-------------------------------|
| Baudrate                      | 38400                         |
| Type                          | dep.Ch                        |
| nChan                         | Chan 2                        |

#### Calibration Proceedure
0. Power Off the SCT-1100 by holding down the `C On/Stb` button
0. Press `C On/Stb` button to power back on
0. While SCT is booting up hold down the `TARE` button
0. Select the `SETUP` option
0. Select the `CONFIG` option
0. Select the `CALIB` option (Not the `0.CALIB` option)
0. `DEC` should appear next on the display.  Press enter (`Print`) to set decimal points to 1.00 (two decimal places)
0. `UN` should appear next.  Press enter (`Print`) to set units to `LB`
0. `DIV` appears next.  Press enter (`Print`) to set divisions to 1
0. `RANGE 1 ` appears next. Press enter (`Print`) and set to 100.00
0. `RANGE 2` appears next.  Press enter (`Print`) and set to 00.000
0. Press enter (`Print`) on `CALIB P` next.  
0. `NTP` appears next.  Press enter (`Print`) and set to number of calibration points (1 is fine)
0. `TP0` appears next.  Ensure no weight is on the scale and press enter (`Print`).  SCT will spend some time zeroing the scale. 
0. `DDT1` appears next.  Press enter (`Print`) to set the value of the first calibration weight
0. `TP1` appears next.  Hang the calibration weight make sure it is stable before pressing enter (`Print`)
0. Repeat for as many calibration points as specified in `NTP`
0. `EQUAL` appears next. Press enter (`Print`) and let it do its thing (Not exactly sure what this does.  It might not be necessary.
0. When completed, press `C On/Stb` a few times until `SAVE?` appears.  Press enter (`Print`) to save configuration.  The SCT will reboot.  
0. The scale should now be calibrated.  Remove the calibration weight and make sure the reading on the SCT returns to 0.  Hang the calibration weight (or ideally a different one) and make sure the scale reads appropriately. 


