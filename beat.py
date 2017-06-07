import glob
import random
from pippi import dsp, rhythm

manys = sorted(glob.glob('manys/*.wav'))

hats = []
claps = []
for i, filename in enumerate(manys):
    if i >= 284 and i <= 345:
        hats += [ dsp.read(filename) ]

    if i >= 346 and i <= 381:
        claps += [ dsp.read(filename) ]

numlayers = 3
numbeats = 32

out = dsp.buffer()
numbars = 32

start = 0
for b in range(numbars):
    for _ in range(numlayers):
        length = int(44100 * random.triangular(4, 7))
        wtype = random.choice(['sine', 'tri', 'line', 'phasor', 'hann'])
        print(wtype)
        bar = rhythm.curve(numbeats, wtype, length=length)
        for pos in bar:
            hat = random.choice(hats)
            hat = hat.env('phasor') * random.triangular(0.25, 1)
            hat = hat.pan(random.random())
            out.dub(hat, pos + start)

        wtype = random.choice(['sine', 'tri', 'hann', 'line', 'phasor'])
        print(wtype)
        bar = rhythm.curve(numbeats, wtype, length=length)
        for pos in bar:
            clap = random.choice(claps)
            clap = clap.env('phasor') * random.triangular(0.25, 1)
            clap = clap.pan(random.random())
            out.dub(clap, pos + start)

    start += length

out.write('beatless.wav')
