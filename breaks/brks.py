import random
from pippi import dsp

coke = dsp.read('breaks/ike_turner12.flac')
beat = len(coke) // 12

beats = [ b.env('phasor') for b in coke.grains(beat) ]

out = dsp.buffer()
numpasses = 4
speeds = [0.75, 1, 1.5]

for _ in range(numpasses):
    pos = 0
    total_beats = 64
    for _ in range(total_beats):
        pos += (beat * random.randint(1, 3))

        out.dub(random.choice(beats).speed(random.choice(speeds)) * random.triangular(0.25, 0.5), pos)

#coker = coke.fill(len(out))
#out.dub(coker, 0)

out.write('recoke.flac')
