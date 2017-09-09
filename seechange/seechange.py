from pippi import dsp, oscs, tune, rhythm, wavetables
import random
import time
import multiprocessing as mp

start_time = time.time()

osc = oscs.Osc()
out = dsp.buffer()

chords = ['i9', 'ii7', 'IV7', 'i9', 'ii7', 'IV69'] * 4 + ['I']

def make_grain(freqs):
    amp = random.triangular(0, 0.02)

    osc.pulsewidth = random.random()
    osc.window = wavetables.window('random', 512)
    osc.mod = wavetables.window('random', 512)
    osc.mod_range = random.triangular(0, 0.08)
    if osc.mod_range > 0.015:
        osc.mod_freq = random.triangular(0.001, 0.1)
    else:
        osc.mod_freq = random.triangular(0.05, 15)

    osc.wavetable = wavetables.wavetable('random', 512)
    osc.freq = random.choice(freqs) * 2**random.randint(0, 4) * 0.5

    grain = osc.play(random.randint(441, 44100 * 8)) * amp
    grain = grain.env('random').pan(random.random())

    return grain

def make_layer(i, freqs):
    out = dsp.buffer()
    numbeats = random.randint(2, 16)
    length = 44100 * random.randint(2, 12)
    onsets = rhythm.curve(numbeats, 'random', length)
    print('layer', i, 'numbeats', numbeats, 'length', length / 44100)
    for onset in onsets:
        grain = make_grain(freqs)
        out.dub(grain, onset)

    return out


pos = 0
for i, chord in enumerate(chords):
    freqs = tune.chord(chord)
    numlayers = random.randint(10, 30)
    print('chord', chord, i, 'of', len(chords), 'numlayers', numlayers)

    with mp.Pool(processes=4) as pool:
        layers = [ pool.apply_async(make_layer, (i, freqs,)) for i in range(numlayers) ]

        for result in layers:
            layer = result.get()
            out.dub(layer, pos)

    pos = len(out) - random.randint(44100, 44100 * 6)


out.write('seechanges.wav')
elapsed_time = time.time() - start_time
print('Render time: %s seconds' % round(elapsed_time, 2))
print('Output length: %s seconds' % round(len(out)/44100, 2))
