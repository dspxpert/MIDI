import rtmidi
import time

def major_chord(ch, note, midiout, delay=1):
    # tonic
    midiout.send_message([0x90 + ch, note, 112])
    time.sleep(delay)

    # midiant
    midiout.send_message([0x90 + ch, note + 4, 112])
    time.sleep(delay)
    
    # dominant
    midiout.send_message([0x90 + ch, note + 7, 112])
    time.sleep(delay)
    time.sleep(0.5)
    
    # notes off
    midiout.send_message([0x80 + ch, note, 112])
    midiout.send_message([0x80 + ch, note + 4, 112])
    midiout.send_message([0x80 + ch, note + 7, 112])
    
    time.sleep(0.1)
    
out = rtmidi.MidiOut()

ports_dict = {k: v for (v, k) in enumerate(out.get_ports())}
out.open_port(ports_dict['VirtualMIDISynth #1 0'])

with out:
    major_chord(0, 48, out)  # 48 C3
    major_chord(0, 60, out)  # 60 C4(middle C)
    major_chord(0, 72, out)  # 72 C5
    major_chord(0, 72, out, delay = 0)
    time.sleep(0.1)
    
del out