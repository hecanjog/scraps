import random
import time
import numpy as np
from pippi import dsp, wavetables, interpolation
from pippi.soundbuffer import SoundBuffer

start_time = time.time()

def make_wta(freq, length, probt, jittert):
    wt = []
    wlen = int(44100 / freq)
    elapsed = 0
    count = 0

    wform = wavetables.random_wavetable()
    prob = 1
    jitter = 0
    while elapsed < length:
        print('   %s, %s' % (prob, jitter))

        if random.random() >= prob:
            wform = wavetables.random_wavetable()

        prob = probt[count % len(probt)] * 0.03 + 0.97
        jitter = jittert[count % len(jittert)] * 50

        """
        prob += random.triangular(-0.001, 0.002)
        if prob > 1:
            prob = 1
        elif prob < 0.98:
            prob = 0.98
        elif prob < 0.99:
            prob += random.triangular(0.001, 0.02)

# jitter 0-1 * 100
# prob 0-1 * 0.02 + 0.98

        jitter += random.triangular(-1, 1.5)
        if jitter > 30:
            jitter = 30
        elif jitter < 0:
            jitter = 0
        elif jitter > 10:
            jitter += random.triangular(-2, 1)
        """

        w = wavetables.wavetable(wform, wlen)
        win = wavetables.window('sine', wlen)
        wo = [ w[i] * win[i] for i in range(wlen) ]
        if len(wt) > 0:
            joiner = interpolation.linear([wt[-1], wo[0]], random.randint(wlen, wlen+int(jitter)))
            wo = list(joiner) + wo
        wt += wo
        elapsed += len(w)
        count += 1

    return wt

def make_wt(length):
    wt = []
    maxlen = int(length / 1000)

    elapsed = 0
    count = 0
    while elapsed < length:
        w = wavetables.window('random', random.randint(1, maxlen))
        wt += w
        elapsed += len(w)
        count += 1

    slop = length - len(wt)
    if slop > 0:
        wt += wavetables.window('random', slop)

    return wt

def make_tone(freq, length, probt, jittert):
    wtsize = 4096 * 2
    num_wts = 3

    print('making %s %s wavetables' % (num_wts, wtsize))
    wts = []
    for _ in range(num_wts):
        wts += [ make_wt(wtsize) ]

    print('making mod table')
    mod = make_wt(wtsize)

    print('interpolating tables')
    fwt = interpolation.interp2d(wts, mod, wtsize)
    """
    fwt = []
    for i in range(wtsize):
        vwt = interpolation.linear([ w[i] for w in wts ], wtsize)
        modi = int(mod[i] * (len(vwt) -1))
        val = vwt[modi]
        fwt += [ val ]
    """
        
    #s = np.array(make_wta(freq, length, probt, jittert))
    #s = np.column_stack((s, s))
    print('synthesizing tone %shz %s' % (freq, length / 44100))
    s = make_wta(freq, length, probt, jittert)

    print('converting to soundbuffer and multiplying by wavetables')
    out = SoundBuffer(frames=s, channels=2, samplerate=44100) * 0.05
    return out * fwt

out = dsp.buffer()
bf = 55.125
freqs = [bf, bf*2, bf*3, bf*4, bf*6, bf*8]

pos = 0
numtones = 4
wtsize = 4096 * 10
tone_params = []
for _ in range(numtones):
    tone_params += [ (random.choice(freqs) * 2**random.randint(0,2) * random.choice([1, 1.5, 1, 1, 1]), random.randint(44100 * 5, 44100 * 10), make_wt(wtsize), make_wt(wtsize)) ]

print('async pool of %s tone renders' % numtones)
tones = dsp.pool(make_tone, tone_params)

print('enveloping panning and dubbing tones')
for t in tones:
    print('tone', _, 'pos', round(pos, 4))
    t = t.env('sine')
    t = t.pan(random.random())
    out.dub(t, pos)
    pos += random.randint(100, 44100)

out.write('amaker.wav')
elapsed_time = time.time() - start_time
print('Render time: %s seconds' % round(elapsed_time, 2))
print('Output length: %s seconds' % round(len(out)/44100, 2))
