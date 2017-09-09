import random
from pippi import dsp, tune

harp = dsp.read('harps/harp_100.wav')
#harp = dsp.read('manys/many_612.wav')

#freqs = tune.chord('I69')
freqs = [ 55 * (i+1) for i in range(6) ]

out = dsp.silence(1)

num_grains = 1000
for _ in range(num_grains):
    wt = [ random.random() for _ in range(random.randint(3, 10)) ]
    grain_length = random.randint(int(44100 * 1), int(44100 * 2))
    freq = random.choice(freqs) * 2**random.randint(0, 6)
    grain = harp.rcut(grain_length).env(values=wt)
    grain = grain.speed(freq/440).env('sine') * random.random()
    grain = grain.pan(random.random(), 'linear')

    out.dub(grain, random.randint(0, 44100 * 90))

out.write('harpy.wav')
