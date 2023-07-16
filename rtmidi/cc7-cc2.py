import rtmidi
import time

midi_in = rtmidi.MidiIn()
midi_out = rtmidi.MidiOut()


ports_dict = {k: v for (v, k) in enumerate(midi_in.get_ports())}
print(ports_dict)
midi_in.open_port(ports_dict['USB MIDI 3'])

ports_dict = {k: v for (v, k) in enumerate(midi_out.get_ports())}
print(ports_dict)
midi_out.open_port(ports_dict['loopMIDI Port 2'])

while True:
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
