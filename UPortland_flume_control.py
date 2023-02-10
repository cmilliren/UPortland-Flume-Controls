import json
import time
import datetime
import threading
import matplotlib.animation as animation
import SAFL_tkinter_toolbox as safl
import Lenze_VFD_funcs as lenze
import Analog_VFD_controls as analog_vfd
import ADAM_4024_AnalogOut as adam
import Arduino_DigitalOutput as arduino
import BadgerMeter_funcs as badger
import Sedflux_control_funcs as sedflux
import SCT1100_ASCII_funcs as sct
import PXR_Temperature_Funcs as pxr
import Massa_funcs as massa





# initialize the gui (also reads the configs.json file)
gui = safl.gui('UPortland Flume Control Software')

# Define the exit function with all the steps needed to properly close the program. 
def gui_exit():

    #Stop all pumps/motors
    main_pump.stop_pump()
    fill_pump.stop_vfd()
    empty_pump.stop_vfd()
    sed_auger.stop_vfd()
    eductor_pump.stop_vfd()

    #disable the Sed dump motor
    do.disable_teknic_motor()


    #Update the Config.json file.
    gui.configs['Main Pump COM Port']     = main_VFD_comm_selector.port.get()
    gui.configs['Flowmeter COM Port']     = flowmeter_comm_selector.port.get()
    gui.configs['Analog Pumps COM Port']  = analog_VFD_comm_selector.port.get()
    gui.configs['Arduino COM Port']       = arduino_comm_selector.port.get()
    gui.configs['SCT COM Port']           = sct_comm_selector.port.get()
    gui.configs['PXR COM Port']           = pxr_comm_selector.port.get()
    gui.configs['Massa COM Port']         = massa_comm_selector.port.get()
    gui.configs['PlotUpdateRate']         = update_rate_entry.entry.get()
    gui.configs['PlotLength']             = plot_length_entry.entry.get()
    gui.configs['Sed Dump Weight']        = sed_weight_setpoint_input.entry.get()
    gui.configs['Flume Massa Offset']     = massas.offsets[0]
    gui.configs['Tanks Massa Offset']     = massas.offsets[1]


    with open('Config.json','w') as fid: 
        json.dump(gui.configs,fid)
    print('Closing GUI')
    gui.window.destroy()


# initialize all measurement/control devices.
ao = adam.adam4024(gui.configs['Analog Pumps COM Port'],1)
do = arduino.digout(gui.configs['Arduino COM Port'])

main_pump    = lenze.lenze_vfd(gui.configs['Main Pump COM Port'],1)
fill_pump    = analog_vfd.vfd(0,ao,do)
empty_pump   = analog_vfd.vfd(1,ao,do)
eductor_pump = analog_vfd.vfd(3,ao,do)
sed_auger    = analog_vfd.vfd(2,ao,do)
flowmeter    = badger.badger_flowmeter(gui.configs['Flowmeter COM Port'],1)
load_cells   = sct.SCT1100(gui.configs['SCT COM Port'])
sed_flux     = sedflux.sed_flux_control(gui.configs['Sed Dump Weight'],do,load_cells)
water_temp   = pxr.pxr(gui.configs['PXR COM Port'],1)
massas       = massa.massa(gui.configs['Massa COM Port'],[1,2],[float(gui.configs['Flume Massa Offset']),float(gui.configs['Tanks Massa Offset'])])



#Configure the GUI Structure
gui.add_tabs(['Home','Datalogging','Settings'])


# Layout Home Page:
gui.add_frame(gui.tabs['Home'],'Flume Controls')
gui.add_frame(gui.tabs['Home'],'Real Time Data')
gui.add_frame(gui.tabs['Home'],'Sed Flux Controls')


gui.add_frame_below(gui.frames['Flume Controls'],'System Status')
gui.add_frame_below(gui.frames['Flume Controls'],'Water')
gui.add_frame_below(gui.frames['Flume Controls'],'Pump Controls')
gui.add_frame_below(gui.frames['Pump Controls'],'Main Pump')
gui.add_frame_below(gui.frames['Pump Controls'],'Fill Pump')
gui.add_frame_below(gui.frames['Pump Controls'],'Empty Pump')
gui.add_frame_below(gui.frames['Sed Flux Controls'],'Sed Flux')
gui.add_frame_below(gui.frames['Sed Flux'],'Sed Feed Auger')
gui.add_frame_below(gui.frames['Sed Flux'],'Eductor Pump')
gui.add_frame_below(gui.frames['Sed Flux'],'Weigh Pan')


# Home Page - Plots
flowrate_plot = safl.live_data_plot(gui.frames['Real Time Data'],int(gui.configs['PlotLength']),1,'Water Flowrate','lps',['Flowrate'])
sed_flux_plot = safl.live_data_plot(gui.frames['Real Time Data'],int(gui.configs['PlotLength']),1,'Sediment Weight','lbs',['Weigh Pan'])

# Home Page - System Status 
time_loop = safl.timestamp_looptime(gui.frames['System Status'])
skipped_scans = safl.value_display(gui.frames['System Status'],'Loop Time Overruns')
logging_status_display = safl.value_display(gui.frames['System Status'],'Datalogging Status')
missed_records = safl.value_display(gui.frames['System Status'],'Missed Data Records')

# Home Page - Temperature
flowrate_display = safl.value_display(gui.frames['Water'],'Flowrate')
water_temp_display = safl.value_display(gui.frames['Water'],'Water Temperature')
flume_depth_display = safl.value_display(gui.frames['Water'],'Flume Water Depth')
tank_depth_display  = safl.value_display(gui.frames['Water'],'Storage Tanks Water Level')

# Home Page - Flume Controls
main_pump_status_display = safl.value_display(gui.frames['Main Pump'],'Comm Status')
main_pump_error_display = safl.value_display(gui.frames['Main Pump'],'Errors')
main_pump_running_distplay = safl.value_display(gui.frames['Main Pump'],'Pump Status')
main_pump_setpoint_display = safl.value_display(gui.frames['Main Pump'],'Current Setpoint')
main_pump_setpoint_input = safl.setpoint_input(gui.frames['Main Pump'],'Frequency Setpoint (0-60 Hz)','Set',main_pump.send_setpoint,default_value=30)
main_pump_start_stop = safl.start_stop_reset_buttons(gui.frames['Main Pump'],main_pump.start_pump,main_pump.stop_pump,main_pump.reset_fault)

fill_pump_setpoint_display = safl.value_display(gui.frames['Fill Pump'],'Current Setpoint')
fill_pump_status_display   = safl.value_display(gui.frames['Fill Pump'],'Status')
fill_pump_setpoint_input = safl.setpoint_input(gui.frames['Fill Pump'],'Frequency Setpoint (0-60 Hz)','Set',fill_pump.set_freq,default_value=60)
fill_pump_start_stop = safl.start_stop_buttons(gui.frames['Fill Pump'],fill_pump.start_vfd,fill_pump.stop_vfd)

empty_pump_setpoint_display = safl.value_display(gui.frames['Empty Pump'],'Current Setpoint')
empty_pump_status_display   = safl.value_display(gui.frames['Empty Pump'],'Status')
empty_pump_setpoint_input = safl.setpoint_input(gui.frames['Empty Pump'],'Frequency Setpoint (0-60 Hz)','Set',empty_pump.set_freq,default_value=60)
empty_pump_start_stop = safl.start_stop_buttons(gui.frames['Empty Pump'],empty_pump.start_vfd,empty_pump.stop_vfd)

eductor_pump_setpoint_display = safl.value_display(gui.frames['Eductor Pump'],'Current Setpoint')
eductor_pump_status_display   = safl.value_display(gui.frames['Eductor Pump'],'Status')
eductor_pump_setpoint_input = safl.setpoint_input(gui.frames['Eductor Pump'],'Frequency Setpoint (0-60 Hz)','Set',eductor_pump.set_freq,default_value=60)
eductor_pump_start_stop = safl.start_stop_buttons(gui.frames['Eductor Pump'],eductor_pump.start_vfd,eductor_pump.stop_vfd)

sed_auger_setpoint_display = safl.value_display(gui.frames['Sed Feed Auger'],'Current Setpoint')
sed_auger_status_display   = safl.value_display(gui.frames['Sed Feed Auger'],'Status')
sed_auger_setpoint_input = safl.setpoint_input(gui.frames['Sed Feed Auger'],'Frequency Setpoint (0-60 Hz)','Set',sed_auger.set_freq,default_value=5)
sed_auger_start_stop = safl.start_stop_buttons(gui.frames['Sed Feed Auger'],sed_auger.start_vfd,sed_auger.stop_vfd)

sed_weight_display = safl.value_display(gui.frames['Weigh Pan'],'Current Weight')
sed_weight_status  = safl.value_display(gui.frames['Weigh Pan'],'Scale Status')
sed_dump_weight_display = safl.value_display(gui.frames['Weigh Pan'],'Current Dump Weight Setpoint')
sed_weight_setpoint_input = safl.setpoint_input(gui.frames['Weigh Pan'],'Dump Weight Setpoint','Set',sed_flux.set_dump_weight,default_value=gui.configs['Sed Dump Weight'])
sed_motor_status = safl.value_display(gui.frames['Weigh Pan'],'Dump Motor Status')
sed_enable_disable = safl.two_buttons(gui.frames['Weigh Pan'],['Enable Dump Motor','Disable Dump Motor'],do.enable_teknic_motor,do.disable_teknic_motor)
sed_tare_dump  = safl.two_buttons(gui.frames['Weigh Pan'],['Tare','Manual Dump'],sed_flux.tare,do.dump_sed)

#Layout for Datalogging Page
datalog = safl.log_data(gui.tabs['Datalogging'])

# Layout for Settings Page
gui.add_frame(gui.tabs['Settings'],'WARNING!')
gui.add_frame(gui.tabs['Settings'],'Massas')
gui.add_frame(gui.tabs['Settings'],'COM Ports')
gui.add_frame(gui.tabs['Settings'],'Program Settings')

flume_massa_settings = safl.massa_settings(gui.frames['Massas'],'Flume Massa',1,massas.update_offset)
tanks_massa_settings = safl.massa_settings(gui.frames['Massas'],'Tanks Massa',2,massas.update_offset)

main_VFD_comm_selector   = safl.COM_Port_Selector(gui.frames['COM Ports'],'Main Pump','Main Pump VFD',gui.configs,'Main Pump COM Port')
flowmeter_comm_selector  = safl.COM_Port_Selector(gui.frames['COM Ports'],'Flowmeter',' Badger Flowmeter',gui.configs,'Flowmeter COM Port')
analog_VFD_comm_selector = safl.COM_Port_Selector(gui.frames['COM Ports'],'Analog Pump Control','ADAM-4024',gui.configs,'Analog Pumps COM Port')
arduino_comm_selector    = safl.COM_Port_Selector(gui.frames['COM Ports'],'Digital Output Pump Control','Arduino',gui.configs,'Arduino COM Port')
sct_comm_selector        = safl.COM_Port_Selector(gui.frames['COM Ports'],'Sed Flux Load Cells','SCT-1100',gui.configs,'SCT COM Port')
pxr_comm_selector        = safl.COM_Port_Selector(gui.frames['COM Ports'],'Temperature Sensor','Fuji PXR',gui.configs,'PXR COM Port')
massa_comm_selector      = safl.COM_Port_Selector(gui.frames['COM Ports'],'Water Depth Sensor','Massa Ultrasonic(s)',gui.configs,'Massa COM Port')

update_rate_entry = safl.setpoint_input(gui.frames['Program Settings'],'Program Update Rate (ms) : ','Set',print,default_value=gui.configs['PlotUpdateRate'])
plot_length_entry = safl.setpoint_input(gui.frames['Program Settings'],'Plot Length (number of records): ','Set',print,default_value=gui.configs['PlotLength'])
safl.Restart_GUI_Button(gui.frames['WARNING!'],gui_exit)


# Variables for plots:

sed_flux_plotdata = {'ts':'','data':[]}
flowrate_plot_data = {'ts':'','data':[]}

def main_loop():
    tic = time.perf_counter()
    ts = datetime.datetime.now()
    time_loop.update(ts)
    skipped_scans.update(gui.skipped_scans)
    missed_records.update(gui.missed_records)


    # Create Threads to read all sensors/device concurrently.  Make sure all devices that share a comm port are on the same thread to avoid conflicts
    sed_flux_thread = threading.Thread(target=sed_flux.update)
    main_pump_thread = threading.Thread(target=main_pump.poll_status)
    analog_vfd_thread = threading.Thread(target=ao.read_all_setpoints)
    flowmeter_thread  = threading.Thread(target=flowmeter.read_flowrate)
    water_temp_thread = threading.Thread(target=water_temp.read_temperature)
    do_thread = threading.Thread(target=do.poll_status)
    massas_thread = threading.Thread(target=massas.poll_status)

    # Start Threads
    sed_flux_thread.start()
    main_pump_thread.start()
    analog_vfd_thread.start()
    flowmeter_thread.start()
    water_temp_thread.start()
    do_thread.start()
    massas_thread.start()

    # Join Threads so that the program waits for all threads to finish before moving on with the program
    sed_flux_thread.join()
    main_pump_thread.join()
    analog_vfd_thread.join()
    flowmeter_thread.join()
    water_temp_thread.join()
    do_thread.join()
    massas_thread.join()

        # Log data to File
    header = ['Timestamp','Flowrate','Water Depth','Water Temp','Sed Pan Weight','Sed Auger Hz','Main VFD Hz','Fill VFD Hz','Empty VFD Hz','Eductor VFD Hz']
    data = [ts,
            round(flowmeter.flowrate,2),
            round(massas.water_depth_array[0],2),
            round(water_temp.temperature,2),
            round(sed_flux.sct.net_weight,2),
            round(ao.setpoints[2]) if do.sed_auger_enabled == 'Running' else 0,
            round(main_pump.current_setpoint,2) if main_pump.status['RunningForward'] else 0,
            round(ao.setpoints[0],2) if do.fill_pump_enabled == 'Running' else 0,
            round(ao.setpoints[1],2) if do.empty_pump_enabled == 'Running' else 0,
            round(ao.setpoints[3],2) if do.eductor_pump_enabled == 'Running' else 0]
    datalog.write_data(gui,header,data)



    # Update gui with new values: 
    if datalog.status == 'Recording':
        logging_status_display.update(datalog.status,background_color='green')
    else:
        logging_status_display.update(datalog.status,background_color='light gray')

    flowrate_display.update(f'{flowmeter.flowrate:.2f} lps')
    water_temp_display.update(f'{water_temp.temperature:.1f} degC')
    sed_weight_display.update(f'{sed_flux.sct.net_weight:.2f} lbs')
    sed_weight_status.update(f'{sed_flux.sct.scale_status}')
    sed_dump_weight_display.update(f'{sed_flux.dump_weight} lbs')
    fill_pump_setpoint_display.update(f'{ao.setpoints[0]:.1f} Hz')
    fill_pump_status_display.update(f'{do.fill_pump_enabled}')
    empty_pump_setpoint_display.update(f'{ao.setpoints[1]:.1f} Hz')
    empty_pump_status_display.update(f'{do.empty_pump_enabled}')
    eductor_pump_setpoint_display.update(f'{ao.setpoints[3]:.1f} Hz')
    eductor_pump_status_display.update(f'{do.eductor_pump_enabled}')
    sed_auger_setpoint_display.update(f'{ao.setpoints[2]:.1f} Hz')
    sed_auger_status_display.update(f'{do.sed_auger_enabled}')
    main_pump_setpoint_display.update(f'{main_pump.current_setpoint:.1f} Hz')
    main_pump_status_display.update(f"{['Error','OK'][main_pump.comm_OK]}")

    if main_pump.error_code != 0:
        main_pump_error_display.update(main_pump.error_message,background_color='red')
    else:
        main_pump_error_display.update(main_pump.error_message,background_color=gui.window.cget('background'))

    main_pump_running_distplay.update(f"{['Stopped','Running'][main_pump.status['RunningForward']]}")
    sed_motor_status.update(f'{do.teknic_motor_enabled}')
    flume_depth_display.update(f'{massas.water_depth_array[0]:.2f} cm')
    tank_depth_display.update(f'{massas.water_depth_array[1]:.2f} cm')

    flume_massa_settings.update(massas,1)
    tanks_massa_settings.update(massas,2)



    # Update Plots with latest data
    sed_flux_plotdata['ts'] = ts
    sed_flux_plotdata['data'] = [sed_flux.sct.net_weight]

    flowrate_plot_data['ts'] = ts
    flowrate_plot_data['data'] = [flowmeter.flowrate]



    loop_time = time.perf_counter()-tic
    if int(gui.configs['PlotUpdateRate'])-loop_time*1000 < 0:
        print('Skipped Scan! \n Measurements took longer than the specified Update Rate \n Increase Update Rate on Settings Tab \n\n')
        gui.skipped_scans = gui.skipped_scans + 1
        loop_time = 5000 # if loop time is too long
    gui.window.after(int(round(int(gui.configs['PlotUpdateRate'])-loop_time*1000)),main_loop)


def update_sed_flux_plot(i):
    sed_flux_plot.update_plot(sed_flux_plotdata['ts'],sed_flux_plotdata['data'])

def update_flowrate_plot(i):
    flowrate_plot.update_plot(flowrate_plot_data['ts'],flowrate_plot_data['data'])



# Start gui loops running
main_loop()
ani1 = animation.FuncAnimation(sed_flux_plot.figure,update_sed_flux_plot,interval=int(gui.configs['PlotUpdateRate']))
ani2 = animation.FuncAnimation(flowrate_plot.figure,update_flowrate_plot,interval=int(gui.configs['PlotUpdateRate']))



# Set up exit method
gui.window.protocol("WM_DELETE_WINDOW", gui_exit)
# Start GUI.  mainloop() must be the last thing called in the program. 
gui.window.mainloop()

