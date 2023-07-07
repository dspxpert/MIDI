#https://gist.github.com/ChrisWellsWood/c30eed98c2062f0059276587535acc22

import rtmidi
import time

midi_in = rtmidi.MidiIn()

ports_dict = {k: v for (v, k) in enumerate(midi_in.get_ports())}
# midi_in.open_port(ports_dict['loopMIDI Port 0'])
midi_in.open_port(ports_dict['CircuitPython Audio 1'])

while True:
    msg_and_dt = midi_in.get_message()
    
    # check to see if there is a message
    if msg_and_dt:
        # unpack the msg and time tuple
        (msg, dt) = msg_and_dt

        # convert the command integer to a hex so it's easier to read
        command = hex(msg[0])
        print(f"{command} {msg[1:]}\t| dt = {dt:.2f}")
    else:
        # add a short sleep so the while loop doesn't hammer your cpu
        time.sleep(0.001)