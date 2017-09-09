import glob
import random
from pippi import dsp, rhythm

numlayers = 3
numbeats = 32

hats = [ hat for hat in dsp.find('drums/hat*.wav') ]
snares = [ snare for snare in dsp.find('drums/snare*.wav') ]
kicks = [ kick for kick in dsp.find('drums/kick*.wav') ]

drums = [hats, snares, kicks]

out = dsp.buffer()
numbars = 32

start = 0
for b in range(numbars):
    numlayers = random.randint(2, 5)
    for _ in range(numlayers):
        length = int(44100 * random.triangular(4, 7))
        wtype = random.choice(['sine', 'tri', 'line', 'phasor', 'hann'])
        bar = rhythm.curve(numbeats, wtype, length=length)

        for pos in bar:
            sounds = random.choice(drums)
            hat = random.choice(sounds)
            hat = hat.env('phasor') * random.triangular(0.25, 1)
            hat = hat.pan(random.random())
            out.dub(hat, pos + start)

    start += length

out.write('trapbeatless.wav')
