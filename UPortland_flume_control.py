import SAFL_tkinter_toolbox as safl
import Lenze_VFD_funcs as lenze





# initialize the gui (also reads the configs.json file)
gui = safl.gui('UPortland Flume Control Software')

# initialize all measurement/control devices.
main_pump = lenze.lenze_vfd('COM4',1)



#Configure the GUI Structure
gui.add_tabs(['Home','Datalogging','Settings'])


# Define the exit function with all the steps needed to properly close the program. 
def gui_exit():
    # Kill the Paddle Wheel Control .exe file.
    # wheels.kill_exe()

    # #Update the Config.json file.
    # gui.configs['VFD'] = vfds_comm_selector.port.get()
    # gui.configs['Flowmeter'] = flowmeter_comm_selector.port.get()
    # gui.configs['Chiller'] = chiller_comm_selector.port.get()
    # gui.configs['PlotUpdateRate'] = update_rate_entry.entry.get()
    # gui.configs['PlotLength'] = plot_length_entry.entry.get()

    # with open('Config.json','w') as fid: 
    #     json.dump(gui.configs,fid)

    gui.window.destroy()

