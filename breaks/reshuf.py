import random
from pippi import dsp

coke = dsp.read('breaks/coke_escovedo8.flac')
numbeats = 16
beat = len(coke) // numbeats

def get_section():
    start_beat = random.randint(0, numbeats-1)
    beatlength = random.randint(1, numbeats - start_beat)
    bt = coke[start_beat * beat:beatlength * beat]
    print(start_beat, beatlength, beat, len(bt))

    return bt

beats = [ b.env('phasor') for b in coke.grains(beat) ]

out = dsp.buffer()
lenbeats = 64

pos = 0
for _ in range(lenbeats):
    bt = get_section()
    out.dub(bt, pos)
    pos += len(bt)

#coker = coke.fill(len(out))
#out.dub(coker, 0)

out.write('reshuf.flac')
