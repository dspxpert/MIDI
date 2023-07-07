# pip install mido python-rtmidi


import mido
from mido import MidiFile
import time

print(mido.get_output_names())

msg1 = mido.Message('note_on', note=60)
msg2 = mido.Message('note_off', note=60)

#port = mido.open_output('loopMIDI Port 1')
port = mido.open_output('VirtualMIDISynth #1 0')
#port = mido.open_output('Microsoft GS Wavetable Synth 0')

# MIDI message test
while False:
    port.send(msg1)
    time.sleep(1)
    port.send(msg2)
    time.sleep(1)

# MIDI file test
# https://mido.readthedocs.io/en/latest/midi_files.html

for msg in MidiFile('Robert_Miles_-_Children.mid').play():
    port.send(msg)
