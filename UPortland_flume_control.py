import json
import SAFL_tkinter_toolbox as safl
import Lenze_VFD_funcs as lenze
import Analog_VFD_controls as analog_vfd
import ADAM_4024_AnalogOut as adam
import Arduino_DigitalOutput as arduino
import BadgerMeter_funcs as badger
import Sedflux_control_funcs as sedflux
import SCT1100_ASCII_funcs as sct






# initialize the gui (also reads the configs.json file)
gui = safl.gui('UPortland Flume Control Software')

# Define the exit function with all the steps needed to properly close the program. 
def gui_exit():


    #Update the Config.json file.
    gui.configs['Main Pump COM Port'] = main_VFD_comm_selector.port.get()
    gui.configs['Flowmeter COM Port'] = flowmeter_comm_selector.port.get()
    gui.configs['Analog Pumps COM Port'] = analog_VFD_comm_selector.port.get()
    gui.configs['Arduino COM Port'] = arduino_comm_selector.port.get()
    gui.configs['SCT COM Port']     = sct_comm_selector.port.get()
    gui.configs['PXR COM Port']     = pxr_comm_selector.port.get()
    gui.configs['Massa COM Port']   = massa_comm_selector.port.get()
    gui.configs['PlotUpdateRate'] = update_rate_entry.entry.get()
    gui.configs['PlotLength'] = plot_length_entry.entry.get()
    gui.configs['Sed Dump Weight'] = sed_weight_setpoint_input.entry.get()


    with open('Config.json','w') as fid: 
        json.dump(gui.configs,fid)
    print('Closing GUI')
    gui.window.destroy()


# initialize all measurement/control devices.
ao = adam.adam4024(gui.configs['Analog Pumps COM Port'],1)
do = arduino.digout(gui.configs['Arduino COM Port'])

main_pump = lenze.lenze_vfd(gui.configs['Main Pump COM Port'],1)
fill_pump    = analog_vfd.vfd(0,ao,do)
empty_pump   = analog_vfd.vfd(1,ao,do)
eductor_pump = analog_vfd.vfd(2,ao,do)
sed_auger    = analog_vfd.vfd(3,ao,do)
flowmeter    = badger.badger_flowmeter(gui.configs['Flowmeter COM Port'],1)
load_cells   = sct.SCT1100(gui.configs['SCT COM Port'])
sed_flux     = sedflux.sed_flux_control(gui.configs['Sed Dump Weight'])



#Configure the GUI Structure
gui.add_tabs(['Home','Datalogging','Settings'])


# Layout Home Page:
gui.add_frame(gui.tabs['Home'],'Real Time Data')
gui.add_frame(gui.tabs['Home'],'Flume Controls')
gui.add_frame_below(gui.frames['Flume Controls'],'System Status')
gui.add_frame_below(gui.frames['Flume Controls'],'Pump Controls')
gui.add_frame_below(gui.frames['Pump Controls'],'Main Pump')
gui.add_frame_below(gui.frames['Pump Controls'],'Fill Pump')
gui.add_frame_below(gui.frames['Pump Controls'],'Empty Pump')
gui.add_frame_below(gui.frames['Flume Controls'],'Sed Flux')
gui.add_frame_below(gui.frames['Sed Flux'],'Sed Feed Auger')
gui.add_frame_below(gui.frames['Sed Flux'],'Eductor Pump')
gui.add_frame_below(gui.frames['Sed Flux'],'Weigh Pan')


# Home Page - Plots
flowrate_plot = safl.live_data_plot(gui.frames['Real Time Data'],int(gui.configs['PlotLength']),1,'Water Flowrate','lps',['Flowrate'])
sed_flux_plot = safl.live_data_plot(gui.frames['Real Time Data'],int(gui.configs['PlotLength']),1,'Sediment Weight','lbs',['Weigh Pan'])

# Home Page - System Status 
time_loop = safl.timestamp_looptime(gui.frames['System Status'])
skipped_scans = safl.value_display(gui.frames['System Status'],'Loop Time Overruns:')
# missed_records = safl.value_display(gui.frames['System Status'],'Missed Data Records:')

# Home Page - Flume Controls
# flowrate_display = safl.value_display(gui.frames['Pump Controls'],'Measured Flowrate')
main_pump_status_display = safl.value_display(gui.frames['Main Pump'],'Status')
main_pump_setpoint_display = safl.value_display(gui.frames['Main Pump'],'Current Setpoint')
main_pump_setpoint_input = safl.setpoint_input(gui.frames['Main Pump'],'Frequency Setpoint (0-60 Hz)','Set',main_pump.send_setpoint,default_value=30)
main_pump_start_stop = safl.start_stop_reset_buttons(gui.frames['Main Pump'],main_pump.start_pump,main_pump.stop_pump,main_pump.reset_fault)

fill_pump_setpoint_display = safl.value_display(gui.frames['Fill Pump'],'Current Setpoint')
fill_pump_setpoint_input = safl.setpoint_input(gui.frames['Fill Pump'],'Frequency Setpoint (0-60 Hz)','Set',fill_pump.set_freq,default_value=60)
fill_pump_start_stop = safl.start_stop_buttons(gui.frames['Fill Pump'],fill_pump.start_vfd,fill_pump.stop_vfd)

empty_pump_setpoint_display = safl.value_display(gui.frames['Empty Pump'],'Current Setpoint')
empty_pump_setpoint_input = safl.setpoint_input(gui.frames['Empty Pump'],'Frequency Setpoint (0-60 Hz)','Set',empty_pump.set_freq,default_value=60)
empty_pump_start_stop = safl.start_stop_buttons(gui.frames['Empty Pump'],empty_pump.start_vfd,empty_pump.stop_vfd)

eductor_pump_setpoint_display = safl.value_display(gui.frames['Eductor Pump'],'Current Setpoint')
eductor_pump_setpoint_input = safl.setpoint_input(gui.frames['Eductor Pump'],'Frequency Setpoint (0-60 Hz)','Set',eductor_pump.set_freq,default_value=60)
eductor_pump_start_stop = safl.start_stop_buttons(gui.frames['Eductor Pump'],eductor_pump.start_vfd,eductor_pump.stop_vfd)

sed_auger_setpoint_display = safl.value_display(gui.frames['Sed Feed Auger'],'Current Setpoint')
sed_auger_setpoint_input = safl.setpoint_input(gui.frames['Sed Feed Auger'],'Frequency Setpoint (0-60 Hz)','Set',sed_auger.set_freq,default_value=5)
sed_auger_start_stop = safl.start_stop_buttons(gui.frames['Sed Feed Auger'],sed_auger.start_vfd,sed_auger.stop_vfd)

sed_weight_display = safl.value_display(gui.frames['Weigh Pan'],'Current Weight')
sed_weight_setpoint_input = safl.setpoint_input(gui.frames['Weigh Pan'],'Dump Weight Setpoint','Set',sed_flux.set_dump_weight,default_value=gui.configs['Sed Dump Weight'])
sed_manual_dump  = safl.one_button(gui.frames['Weigh Pan'],'Manual Dump',do.dump_sed)

# Layout for Settings Page
gui.add_frame(gui.tabs['Settings'],'WARNING!')
gui.add_frame(gui.tabs['Settings'],'COM Ports')
gui.add_frame(gui.tabs['Settings'],'Program Settings')
main_VFD_comm_selector   = safl.COM_Port_Selector(gui.frames['COM Ports'],'Main Pump','Main Pump VFD',gui.configs,'Main Pump COM Port')
flowmeter_comm_selector  = safl.COM_Port_Selector(gui.frames['COM Ports'],'Flowmeter',' Badger Flowmeter',gui.configs,'Flowmeter COM Port')
analog_VFD_comm_selector = safl.COM_Port_Selector(gui.frames['COM Ports'],'Analog Pump Control','ADAM-4024',gui.configs,'Analog Pumps COM Port')
arduino_comm_selector    = safl.COM_Port_Selector(gui.frames['COM Ports'],'Digital Output Pump Control','Arduino',gui.configs,'Arduino COM Port')
sct_comm_selector        = safl.COM_Port_Selector(gui.frames['COM Ports'],'Sed Flex Load Cells','SCT-1100',gui.configs,'SCT COM Port')
pxr_comm_selector        = safl.COM_Port_Selector(gui.frames['COM Ports'],'Temperature Sensor','Fuji PXR',gui.configs,'PXR COM Port')
massa_comm_selector      = safl.COM_Port_Selector(gui.frames['COM Ports'],'Water Depth Sensor','Massa Ultrasonic(s)',gui.configs,'Massa COM Port')

update_rate_entry = safl.setpoint_input(gui.frames['Program Settings'],'Program Update Rate (ms) : ','Set',print,default_value=gui.configs['PlotUpdateRate'])
plot_length_entry = safl.setpoint_input(gui.frames['Program Settings'],'Plot Length (number of records): ','Set',print,default_value=gui.configs['PlotLength'])
safl.Restart_GUI_Button(gui.frames['WARNING!'],gui_exit)




gui.window.protocol("WM_DELETE_WINDOW", gui_exit)
gui.window.mainloop()

