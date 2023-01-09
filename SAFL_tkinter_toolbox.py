import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import collections
import datetime
import os,sys
import json
import numpy as np
import threading

class gui(): # Creates a GUI Window when gui.window.mainloop() is called (must be the last line of the script its in)
    def __init__(self,title_string,**kwargs):

        #Initialize the window and set size of the window
        self.window= tk.Tk()
        #window.attributes('-fullscreen',True)
        # self.window.geometry('1200x600')
        #window.configure(background='white')

        # Give the window a title.
        self.window.title(title_string)
        if 'icon' in kwargs:
            self.window.iconbitmap(kwargs['icon'])

        self.frames = {} # allocate a dictionary for frames to be added to.
        self.tabs = {} # allocate a dictionary for tabs to be added to.

        self.skipped_scans = 0
        self.missed_records = 0

        if os.path.exists('Config.json'):
           with open('Config.json','r') as fid: 
                self.configs = json.load(fid)

    def add_tabs(self,tab_names_list):

        s = ttk.Style()
        s.configure('TNotebook.Tab', font=('URW Gothic L','11','bold') )

        self.nb = ttk.Notebook(self.window) ##make notebook to be filled with tabs.

        for i in tab_names_list:
            self.tabs[i] = ttk.Frame(self.nb)
            self.nb.add(self.tabs[i],text = i)

        self.nb.pack(fill=tk.BOTH,expand=True,side=tk.LEFT)

        self.nb.select(self.tabs[tab_names_list[0]]) # Start the GUI on page 1

    def add_frame(self,container,name):
        self.frames[name] = tk.LabelFrame(container,text=name,font=('Arial',12))
        self.frames[name].pack(fill=tk.BOTH,expand=True,side=tk.LEFT)

    def add_frame_below(self,container,name):
        self.frames[name] = tk.LabelFrame(container,text=name,font=('Arial',11,'italic'))
        self.frames[name].pack(fill=tk.X,side=tk.TOP)

    def add_tabs_in_frame(self,container,tab_names_list):
        self.nb_1 = ttk.Notebook(container)

        for i in tab_names_list:
            self.tabs[i] = ttk.Frame(self.nb_1)
            self.nb_1.add(self.tabs[i],text = i)

        self.nb_1.pack(fill=tk.BOTH,expand=True)

        self.nb_1.select(self.tabs[tab_names_list[0]]) # Start the GUI on page 1

    def update_configs(self,param_name,new_value):
        self.configs[param_name] = new_value


class value_display():
    def __init__(self,container,name_str):
        self.frame = tk.Frame(container,pady =2)
        self.frame.pack(fill=tk.X)

        self.value_label = tk.Label(self.frame,text = name_str ,font=('Calibri',10,'bold'),anchor='e',width=30,padx=4)
        self.value_label.pack(side=tk.LEFT)

        self.value = tk.Label(self.frame,text = '#####' ,font=('Calibri',10),anchor='w',width=30)#,padx=4)
        self.value.pack(side = tk.LEFT)

    def update(self,new_value):
        self.value['text'] = str(new_value)

class current_status_setpoint():
    def __init__(self,container):
        self.frame = tk.Frame(container)
        self.frame.pack(fill=tk.X)

        self.status_label = tk.Label(self.frame,text='Current Status: ', font=('Calibri',10),width=18,anchor='e')
        self.status_label.pack(side=tk.LEFT)

        self.status = tk.Label(self.frame,text='Updating...',font=('Calibri',10,'italic'))
        self.status.pack(side=tk.LEFT)

        self.frame1 = tk.Frame(container)
        self.frame1.pack(fill=tk.X)

        self.setpoint_label = tk.Label(self.frame1,text='Current Setpoint: ',font=('Calibri',10),width=18,anchor='e')
        self.setpoint_label.pack(side=tk.LEFT)

        self.setpoint = tk.Label(self.frame1,text='Updating...',font=('Calibri',10,'italic'))
        self.setpoint.pack(side=tk.LEFT)

    def update(self,status,setpoint):
        self.status['text'] = str(status)
        self.setpoint['text'] = str(setpoint)

class setpoint_input():
    ''' 
    Creates a widget with a label, entry box and "set" button that looks like the following

    __________    ______________    ___________
   |  Label   |  |  Entry       |  |   Set     |
    __________    ______________    ___________

   This widget takes up 1 row and 3 columns in the GUI and is arranged using the 'grid' function

   Button action is set with "button_action" input argument
    '''

    def __init__(self,container,title_text,button_text,button_action,**kwargs):
        self.frame = tk.Frame(container,pady=2)
        self.frame.pack(fill=tk.X)
        self.label =  tk.Label(self.frame,text=title_text,font=('Calibri',10,'bold'),width=30,padx=4,anchor='e')
        self.entry =  tk.Entry(self.frame,font=('Calibri',10),width=5)
        self.button = tk.Button(self.frame,text=button_text,font=('Calibri',10),command=lambda:self.button_command(button_action),anchor='e',padx=4)

        if 'default_value' in kwargs:
            self.entry.insert(0,kwargs['default_value'])

        self.label.pack(side=tk.LEFT,padx=4)
        self.entry.pack(side=tk.LEFT)#,padx=4)
        self.button.pack(side=tk.LEFT,padx=4)

    def button_command(self,button_action):
        self.val = self.entry.get()
        button_action(float(self.val))

class gui_configs_update_input():
    ''' 
    Creates a widget with a label, entry box and "set" button that looks like the following

    __________    ______________    ___________
   |  Label   |  |  Entry       |  |   Set     |
    __________    ______________    ___________

   This widget takes up 1 row and 3 columns in the GUI and is arranged using the 'grid' function

   Button action is set with "button_action" input argument
    '''

    def __init__(self,container,title_text,button_text,configs_dict,config_param_name,**kwargs):
        self.frame = tk.Frame(container,pady=2)
        self.frame.pack(fill=tk.X)
        self.label =  tk.Label(self.frame,text=title_text,font=('Calibri',10,'bold'),width=30,padx=4,anchor='e')
        self.entry =  tk.Entry(self.frame,font=('Calibri',10),width=5)
        self.button = tk.Button(self.frame,text=button_text,font=('Calibri',10),command=lambda:self.button_command(configs_dict,config_param_name),anchor='e',padx=4)

        if 'default_value' in kwargs:
            self.entry.insert(0,kwargs['default_value'])

        self.label.pack(side=tk.LEFT,padx=4)
        self.entry.pack(side=tk.LEFT,padx=4)
        self.button.pack(side=tk.LEFT,padx=4)

    def button_command(self,configs_dict,config_param_name):
        self.val = self.entry.get()
        # print(len(self.val))
        if len(self.val)>0:
            configs_dict[config_param_name] = self.val

    def update_text(self,new_title_text):
        self.label['text']=new_title_text
        

class Restart_GUI_Button():
    '''
    Creates a widget with a Label and one button below it:

    Label Text goes here: 
    ________________
    | Button       |
    ________________
    '''

    def __init__(self,container,button_action):
        self.frame = tk.Frame(container,pady=2)
        self.frame.pack(fill=tk.X)
        self.label = tk.Message(self.frame,text='The Python Program must be restarted in order for changes to any of the settings on this page to take effect.  Click the button below to restart the program with the new settings. ')
        self.label.pack(fill=tk.X,padx=4,pady=4)
        self.b = tk.Button(self.frame,text = 'Save Settings and Restart Program',font=('Calibri',10),command=lambda:self.button_command(button_action),width=40,bg='red')
        self.b.pack()

    def button_command(self,button_action):
        # close and restart the program
        button_action()
        python = sys.executable
        os.execl(python, python, * sys.argv)


class one_button():
    '''
    Creates a widget with 1 button

    __________  
   |  button 1| 
    __________  
   '''
    def __init__(self,container,button_label,b1_action):
        self.frame = tk.Frame(container,pady=2)
        self.frame.pack(fill=tk.X)
        self.b1 = tk.Button(self.frame,text = button_label,font=('Calibri',10),command=b1_action,width=20)
        # self.b2 = tk.Button(self.frame,text = button_labels[1],font=('Calibri',10),command=b2_action,width = 20)

        # self.start.grid(row=row,column=col,sticky='e')
        # self.stop.grid(row=row,column = col+1)
        # self.reset.grid(row=row,column=col+2,sticky='w')
        # self.b1.pack(side=tk.LEFT,padx=2,pady=2)
        self.b1.pack(padx=2,pady=2)
        # self.b2.pack(side=tk.LEFT,padx=2,pady=2)


class two_buttons():
    '''
    Creates a widget with 2 buttons

    __________    ____________ 
   |  button 1|  |  button 2   |
    __________    ____________ 
   '''
    def __init__(self,container,button_labels,b1_action,b2_action):
        self.frame = tk.Frame(container,pady=2)
        self.frame.pack(fill=tk.X)
        self.b1 = tk.Button(self.frame,text = button_labels[0],font=('Calibri',10),command=b1_action,width=20)
        self.b2 = tk.Button(self.frame,text = button_labels[1],font=('Calibri',10),command=b2_action,width = 20)

        # self.start.grid(row=row,column=col,sticky='e')
        # self.stop.grid(row=row,column = col+1)
        # self.reset.grid(row=row,column=col+2,sticky='w')
        self.b1.pack(side=tk.LEFT,padx=2,pady=2)
        self.b2.pack(side=tk.LEFT,padx=2,pady=2)

class start_stop_buttons():
    '''
    Creates a widget with 2 buttons - START, STOP

    __________    ____________  
   |  Start   |  |  Stop      | 
    __________    ____________  
   '''
    def __init__(self,container,start_action,stop_action):
        self.frame = tk.Frame(container,pady=2)
        self.frame.pack()
        self.start = tk.Button(self.frame,text = 'Start',font=('Calibri',10),command=start_action,width=12)
        self.stop = tk.Button(self.frame,text = 'Stop',font=('Calibri',10),command=stop_action,width=12)
        # self.reset= tk.Button(self.frame,text = 'Clear Errors',font=('Calibri',10),command=reset_action,width=12)

        # self.start.grid(row=row,column=col,sticky='e')
        # self.stop.grid(row=row,column = col+1)
        # self.reset.grid(row=row,column=col+2,sticky='w')
        self.start.pack(side=tk.LEFT,padx=2)
        self.stop.pack(side=tk.LEFT,padx=2)
        # self.reset.pack(side=tk.LEFT,padx=2)
    def disable_buttons(self):
        self.start['state']  = 'disabled'
        self.stop['state']   = 'disabled'
        # self.reset['state']  = 'disabled'

    def enable_buttons(self):
        self.start['state']  = 'normal'
        self.stop['state']   = 'normal'
        # self.reset['state']  = 'normal'

class start_stop_reset_buttons():
    '''
    Creates a widget with 3 buttons - START, STOP and RESET 

    __________    ____________    ___________
   |  Start   |  |  Stop      |  |  Reset    |
    __________    ____________    ___________
   '''
    def __init__(self,container,start_action,stop_action,reset_action):
        self.frame = tk.Frame(container,pady=2)
        self.frame.pack()
        self.start = tk.Button(self.frame,text = 'Start',font=('Calibri',10),command=start_action,width=12)
        self.stop = tk.Button(self.frame,text = 'Stop',font=('Calibri',10),command=stop_action,width=12)
        self.reset= tk.Button(self.frame,text = 'Clear Errors',font=('Calibri',10),command=reset_action,width=12)

        # self.start.grid(row=row,column=col,sticky='e')
        # self.stop.grid(row=row,column = col+1)
        # self.reset.grid(row=row,column=col+2,sticky='w')
        self.start.pack(side=tk.LEFT,padx=2)
        self.stop.pack(side=tk.LEFT,padx=2)
        self.reset.pack(side=tk.LEFT,padx=2)
    def disable_buttons(self):
        self.start['state']  = 'disabled'
        self.stop['state']   = 'disabled'
        self.reset['state']  = 'disabled'

    def enable_buttons(self):
        self.start['state']  = 'normal'
        self.stop['state']   = 'normal'
        self.reset['state']  = 'normal'

class fwd_rev_stop_reset_buttons():
    '''
    Creates a widget with 3 buttons - START, STOP and RESET 

    __________   __________    ____________    ___________
   |  Foward  | |  Reverse |  |  Stop      |  |  Reset    |
    __________   __________    ____________    ___________
   '''
    def __init__(self,container,row,col,forward_action,reverse_action,stop_action,reset_action):
        self.frame = tk.Frame(container)
        self.frame.pack()
        self.forward = tk.Button(self.frame,text = 'Forward',font=('Calibri',10),command=forward_action)
        self.reverse = tk.Button(self.frame,text = 'Reverse',font=('Calibri',10),command=reverse_action)
        self.stop = tk.Button(self.frame,text = 'Stop',font=('Calibri',10),command=stop_action)
        self.reset= tk.Button(self.frame,text = 'Reset',font=('Calibri',10),command=reset_action)

        # self.forward.grid(row=row,column=col,sticky='e')
        # self.reverse.grid(row=row,column=col+1)
        # self.stop.grid(row=row,column = col+2)
        # self.reset.grid(row=row,column=col+3)
        self.forward.pack(side=tk.LEFT)
        self.reverse.pack(side=tk.LEFT)
        self.stop.pack(side=tk.LEFT)
        self.reset.pack(side=tk.LEFT)


class live_data_plot():
    def __init__(self,container,buffersize,num_plots,title,ylabel,legend_lbls):

        self.data_sets = []
        for i in range(num_plots):
            self.data_sets.append(collections.deque([(datetime.datetime.now(),float('nan'))],maxlen=buffersize))

        self.figure = plt.Figure(figsize=(6,2.5), dpi=100)
        self.ax1 = self.figure.add_subplot(111)
        self.line1 = FigureCanvasTkAgg(self.figure, container)

        self.l = []
        for i in range(num_plots):
            temp, = self.ax1.plot(*zip(*self.data_sets[i]))
            self.l.append(temp)

        self.ax1.set_title(title)
        self.ax1.set_ylabel(ylabel)
        self.ax1.grid()

        self.lgnd = self.ax1.legend(legend_lbls,loc='upper left')

        self.line1.get_tk_widget().pack(fill = tk.BOTH,expand = True)

    def update_plot(self,ts,data_points):
        for i in range(len(data_points)):
            self.data_sets[i].append((ts,data_points[i]))
            self.l[i].set_data(*zip(*self.data_sets[i]))

        self.ax1.relim()
        self.ax1.autoscale_view()

class timestamp_looptime():
    def __init__(self,container):
        # Last Loop time
        self.frame = tk.Frame(container)
        self.frame.pack(fill=tk.X)
        self.frame2 = tk.Frame(container)
        self.frame2.pack(fill=tk.X)

        self.timestamp_label = tk.Label(self.frame,text='Current Timestamp:',font=('Calibri',10,'bold'),anchor='e',width=30,padx=4)
        self.timestamp_value = tk.Label(self.frame,text=str(datetime.datetime.now()),font=('Calibri',10),anchor='w',width=25,padx=4)
        self.looptime_label  = tk.Label(self.frame2,text='Last Loop Time:',font=('Calibri',10,'bold'),anchor='e',width=30,padx=4)
        self.looptime_value  = tk.Label(self.frame2,text='### sec',font=('Calibri',10),anchor='w',width=25,padx=4)

        self.timestamp_label.pack(side=tk.LEFT)
        self.timestamp_value.pack(side=tk.LEFT)
        self.looptime_label.pack(side=tk.LEFT)
        self.looptime_value.pack(side=tk.LEFT)

    def update(self,ts):
        last_ts = datetime.datetime.strptime(self.timestamp_value['text'],'%Y-%m-%d %H:%M:%S.%f')
            
        # Update the Timestamp label
        self.timestamp_value['text']=str(ts)

        # Update the Loop time Label
        loop_time = (ts-last_ts)
        self.looptime_value['text'] = str(round((loop_time.seconds+loop_time.microseconds/1000/1000)*1000,3))+'  milliseconds'
        
        
class log_data():
    def __init__(self,container):
        self.frame = tk.Frame(container)
        # self.frame.pack(fill=tk.X)
        self.frame.pack()

        self.label = tk.Label(self.frame,text='Data File name: ',font = ('Calibri',10),width=16,anchor='e')
        self.label.pack(side=tk.LEFT)

        self.file = tk.Label(self.frame,text='DataFile.csv',font=('Courier',10),relief=tk.SUNKEN,bg='white')#,width=20)
        self.file.pack(side=tk.LEFT)

        self.browse_button = tk.Button(self.frame,text='Browse',command=self.select_file)
        self.browse_button.pack(side=tk.LEFT)

        self.default_filepath = os.environ['USERPROFILE'].replace(os.sep,'/')
        self.filename = self.default_filepath+'/Desktop/DataFile.csv'

        self.frame2 = tk.Frame(container)
        self.frame2.pack(fill=tk.X)
        self.toggle_button = tk.Button(self.frame2,text='Start Logging Data',command=self.toggle_datalogging,relief=tk.RAISED,width=40)
        self.toggle_button.pack(side=tk.TOP)#,fill=tk.X)

    def toggle_datalogging(self):
        if self.toggle_button['relief'] == tk.SUNKEN:
            self.toggle_button['relief'] = tk.RAISED
            self.toggle_button['text'] = 'Start Logging Data'
        else:
            self.toggle_button['relief'] = tk.SUNKEN
            self.toggle_button['text'] = 'Stop Logging Data'


    def select_file(self):
        self.filename = fd.asksaveasfilename(defaultextension='.csv')

        # If user doesn't input a file location and filename, save to desktop
        if len(self.filename)==0:
            self.filename = self.default_filepath+'/Desktop/Datalog_'+ datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')+'.csv'

        self.file['text'] = self.filename.split('/')[-1]

    def write_data(self,gui,header,data):
        # Check if the file already exists.  Append to the file if it does
        try:
            if self.toggle_button['relief']  == tk.SUNKEN:
                if os.path.exists(self.filename):
                    with open(self.filename,'a') as fid:
                        for d in range(len(data)):
                            if d == 0:
                                fid.write(str(data[d]))
                            else:
                                fid.write(','+str(data[d]))
                        fid.write('\n')
                else:
                    with open(self.filename,'a') as fid:
                        for h in range(len(header)):
                            if h == 0:
                                fid.write(str(header[h]))
                            else: 
                                fid.write(','+str(header[h]))
                        fid.write('\n')

                        for d in range(len(data)):
                            if d == 0:
                                fid.write(str(data[d]))
                            else:
                                fid.write(','+str(data[d]))
                        fid.write('\n')
        except Exception as e:
            print(e)
            gui.missed_records = gui.missed_records+1

class scrolling_text_box():
    def __init__(self,container,title):
        self.frame = tk.Frame(container)
        self.frame.pack(fill=tk.X)

        self.label = tk.Label(self.frame,text=title,font = ('Calibri',11),width=16,anchor='w')
        self.label.pack(fill=tk.BOTH,expand=True,side=tk.TOP)

        self.text_box = st.ScrolledText(self.frame,font = ("Calibri",10),background='black',foreground='white')
        self.text_box.pack(fill=tk.BOTH,expand=True,side=tk.TOP)
        self.text_box.see('end')

    def add_text(self,text_to_add):
        self.text_box.insert(tk.INSERT,text_to_add)
        self.text_box.see('end')

class COM_Port_Selector():
    def __init__(self,container,title,device_name,config_dict,config_dict_key):
        self.com_ports = ['COM0','COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','COM10','COM11','COM12','COM13','COM14','COM15','COM16','COM17','COM18','COM19','COM20']
        self.port = tk.StringVar()
        self.port.set(config_dict[config_dict_key])

        self.frame = tk.LabelFrame(container,text=title,font=('Calibri',11,'italic'))
        self.frame.pack(anchor='nw',pady=4)
        tk.Label(self.frame,text='Select COM Port for '+device_name,width=50,anchor='w').pack(anchor='w')
        self.com_select = tk.OptionMenu(self.frame,self.port,*self.com_ports)
        self.com_select.pack(anchor='sw')


def popup_warning(title,yes_no_question,yes_action=any,no_action=any):
    response = messagebox.showwarning(title=title,message=yes_no_question )

    if response == 'ok':
        yes_action
    else:
        pass

def h_line(container):
    ttk.Separator(container).pack(fill=tk.X)

class radio_buttons():
    def __init__(self,container,title,number_of_buttons,button_labels):
        self.frame = tk.Frame(container)
        self.frame.pack(fill=tk.X)

        self.label = tk.Label(self.frame,text=title,font=('Calibri',11,'bold'))
        self.label.pack(anchor='w')

        self.value = tk.IntVar()
        self.selected = -1

        for i in range(number_of_buttons):
            tk.Radiobutton(self.frame,text=button_labels[i],value=i,variable=self.value,command=self.update).pack(side=tk.LEFT)

    def update(self):
        self.selected = self.value.get()

class splash_screen():
    def __init__(self):
        # Create object
        splash_root = tk.Tk()
        
        # Adjust size
        splash_root.geometry("200x200")
        
        # Set Label
        splash_label = tk.Label(splash_root,text="Splash Screen",font=18)
        splash_label.pack()
        
        # main window function
        def main(): 
            # destroy splash window
            splash_root.destroy()

        
        # Set Interval
        splash_root.after(3000,main)
        
        splash_thread = threading.Thread(target=splash_root.mainloop)
        splash_thread.start()
        # Execute tkinter
        splash_root.mainloop()





