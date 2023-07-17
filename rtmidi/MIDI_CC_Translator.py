import tkinter as tk
from tkinter import ttk

import rtmidi
import time
import json

stop = 1

def start_cmd():
    global stop
    
    stop = 0
    
    btn_stop['state'] = 'enable'
    btn_start['state'] = 'disabled'
    
    #print(combo_inport.current())
    #print(combo_outport.current())
    midi_in.close_port()
    midi_out.close_port()
    midi_in.open_port(combo_inport.current())
    midi_out.open_port(combo_outport.current())
    print('MIDI ports open')
    print('MIDI translation start')
    status_msg.set('MIDI translation start')
    
    while True:
        root.update()

        if stop == 1:
            print('MIDI translation stop')
            status_msg.set('MIDI translation stop')
            return
        
        msg_and_dt = midi_in.get_message()
        if msg_and_dt:
            # unpack the msg and time tuple
            (msg, dt) = msg_and_dt
            if msg[0] == 0xB0 and msg[1] == inport_cc.get():
                msg[1] = outport_cc.get()
            # convert the command integer to a hex so it's easier to read
            midi_out.send_message(msg)
            command = hex(msg[0])
            print(f"{command} {msg[1:]}\t| dt = {dt:.2f}")
            status_msg.set(f"{command} {msg[1:]}\t| dt = {dt:.2f}")

        else:
            # add a short sleep so the while loop doesn't hammer your cpu
            time.sleep(0.001)

def stop_cmd():
    global stop
    stop = 1
    
    midi_in.close_port()
    midi_out.close_port()
    print('MIDI ports close')
    status_msg.set('MIDI ports close')

    btn_start['state'] = 'enable'
    btn_stop['state'] = 'disabled'

# Load Configuration file cc_config.json
f=open('cc_config.json', 'r')
CONFIG=json.load(f)
f.close()

midi_in = rtmidi.MidiIn()
midi_out = rtmidi.MidiOut()
inports_list = midi_in.get_ports()
outports_list = midi_out.get_ports()

inport_index = -1
for indexi, inport in enumerate(inports_list):
    if inport.find(CONFIG['Inport']) != -1:
        inport_index = indexi
if inport_index < 0:
    inport_index = 0

outport_index = -1
for indexj, outport in enumerate(outports_list):
    if outport.find(CONFIG['Outport']) != -1:
        outport_index = indexj
if outport_index < 0:
    outport_index = 0

root = tk.Tk()
root.title('MIDI CC Translator')
root.resizable(False, False)

inport_cc = tk.IntVar()
outport_cc = tk.IntVar()
status_msg = tk.StringVar()
status_msg.set('Press START...')

inport_cc.set(CONFIG['Inport_cc'])
outport_cc.set(CONFIG['Outport_cc'])

lbl_inport = ttk.Label(root, text='Input MIDI Port')
lbl_inport.grid(row=0, column=0, sticky='w')
lbl_inport.config(font=('Arial', 12))
lbl_outport = ttk.Label(root, text='Output MIDI Port')
lbl_outport.grid(row=0, column=2, sticky='w')
lbl_outport.config(font=('Arial', 12))

combo_inport = ttk.Combobox(root, width=30, height=15, values=inports_list)
combo_inport.grid(row=1, column=0, columnspan=2, sticky='w')
combo_inport.config(font=('Arial', 12))
combo_inport.current(inport_index)

combo_outport = ttk.Combobox(root, width=30, height=15, values=outports_list)
combo_outport.grid(row=1, column=2, columnspan=2, sticky='w')
combo_outport.config(font=('Arial', 12))
combo_outport.current(outport_index)

lbl_inport_cc = ttk.Label(root, text='CC')
lbl_inport_cc.grid(row=2, column=0, sticky='e')
lbl_inport_cc.config(font=('Arial', 12))
entry_inport_cc = ttk.Entry(root, text=inport_cc, width = 10)
entry_inport_cc.grid(row=2, column=1, sticky='w')
entry_inport_cc.config(font=('Arial', 12))
lbl_outport_cc = ttk.Label(root, text='CC')
lbl_outport_cc.grid(row=2, column=2, sticky='e')
lbl_outport_cc.config(font=('Arial', 12))
entry_outport_cc = ttk.Entry(root, text=outport_cc, width = 10)
entry_outport_cc.grid(row=2, column=3, sticky='w')
entry_outport_cc.config(font=('Arial', 12))

s=ttk.Style()  
s.configure('blue.TButton', font=('Arial', 12, 'bold'), foreground='blue')
s.configure('red.TButton', font=('Arial', 12, 'bold'), foreground='red')

btn_start = ttk.Button(root, text='START', style='blue.TButton', command=start_cmd)
btn_start.grid(row=3, column=2, padx=20, pady=5, sticky='news')

btn_stop  = ttk.Button(root, text='STOP', style='red.TButton', command=stop_cmd)
btn_stop.grid(row=3, column=3, padx=20, pady=5, sticky='news')
btn_stop['state'] = 'disabled'

lbl_status_msg = ttk.Label(root, textvariable=status_msg)
lbl_status_msg.config(font=('Arial', 12))
lbl_status_msg.configure(anchor="center")
lbl_status_msg.configure(background='white')
lbl_status_msg.grid(row=4, column=0, columnspan=4, sticky='news')

root.mainloop()