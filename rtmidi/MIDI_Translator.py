import tkinter as tk
from tkinter import ttk

import rtmidi
import time

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
    
    while True:
        root.update()

        if stop == 1:
            print('MIDI translation stop')
            return
        
        msg_and_dt = midi_in.get_message()
        if msg_and_dt:
            # unpack the msg and time tuple
            (msg, dt) = msg_and_dt
            if msg[0] == 0xB0 and msg[1] == 0x07:
                msg[1] = 0x02
            # convert the command integer to a hex so it's easier to read
            midi_out.send_message(msg)
            command = hex(msg[0])
            print(f"{command} {msg[1:]}\t| dt = {dt:.2f}")
        else:
            # add a short sleep so the while loop doesn't hammer your cpu
            time.sleep(0.001)

def stop_cmd():
    global stop
    stop = 1
    
    midi_in.close_port()
    midi_out.close_port()
    print('MIDI ports close')
    btn_start['state'] = 'enable'
    btn_stop['state'] = 'disabled'
    
midi_in = rtmidi.MidiIn()
midi_out = rtmidi.MidiOut()

#inports_dict = {k: v for (v, k) in enumerate(midi_in.get_ports())}
#print(inports_dict)
#midi_in.open_port(ports_dict['USB MIDI 3'])
inports_list = midi_in.get_ports()

#outports_dict = {k: v for (v, k) in enumerate(midi_out.get_ports())}
#print(outports_dict)
#midi_out.open_port(ports_dict['loopMIDI Port 2'])
outports_list = midi_out.get_ports()

root = tk.Tk()
root.title('MIDI Translator')
#root.geometry('400x300')
root.resizable(False, False)

lbl_inport = ttk.Label(root, text='in-port')
lbl_inport.grid(row=0, column=0, sticky='w')
lbl_outport = ttk.Label(root, text='out-port')
lbl_outport.grid(row=0, column=1, sticky='w')

combo_inport = ttk.Combobox(root, width=30, height=15, values=inports_list)
combo_inport.grid(row=1, column=0, sticky='w')
combo_inport.current(0)
combo_outport = ttk.Combobox(root, width=30, height=15, values=outports_list)
combo_outport.grid(row=1, column=1, sticky='w')
combo_outport.current(0)
#button = tk.Button(root, text='Press Me!')
#button.pack()
#button.pack(expand=True)



btn_start = ttk.Button(root, text='START', command=start_cmd)
btn_start.grid(row=2, column=1, sticky='w')

btn_stop  = ttk.Button(root, text='STOP', command=stop_cmd)
btn_stop.grid(row=3, column=1, sticky='w')

btn_stop['state'] = 'disabled'

text_message = tk.Text(root)
text_message.grid(row=2, column=0, sticky='w', rowspan=2)

#scroll = tk.Scrollbar(root, orient='vertical', command=text.yview)


root.mainloop()