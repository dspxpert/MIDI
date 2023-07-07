import rtmidi
import time

out = rtmidi.MidiOut()

ports_dict = {k: v for (v, k) in enumerate(out.get_ports())}
out.open_port(ports_dict['VirtualMIDISynth #1 0'])

with out:
    note_on = [0x90, 48, 112]
    note_off = [0x80, 48, 0]
    
    cc_msg = [0xB0, 3, 0]
    out.send_message(cc_msg)
    time.sleep(0.1)
    
    out.send_message(note_on)
    time.sleep(1)
    
    for cc in range(127):
        cc_msg = [0xB4, 3, cc]
        out.send_message(cc_msg)
        time.sleep(0.1)
    out.send_message(note_off)
    time.sleep(0.1)
