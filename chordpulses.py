import random
from pippi import dsp, rhythm, tune

out = dsp.buffer()

chords = 'I IV'
chordfreqs = [ tune.chord(chord, key='e') for chord in chords.split(' ') ]

numbars = 32
start = 0
for i in range(numbars):
    freqs = chordfreqs[i % len(chordfreqs)]

    length = int(44100 * random.triangular(3, 7))

    numlayers = random.randint(2, 6)
    for _ in range(numlayers):
        wtype = random.choice(['sine', 'tri', 'line', 'phasor', 'hann'])
        numbeats = random.choice([8, 12, 16])
        bar = rhythm.curve(numbeats, wtype, length=length)

        print(wtype)

        freq = random.choice(freqs) * 2**random.randint(0, 2)
        for pos in bar:
            note = dsp.read('vibesc1.wav')
            note = note.speed(freq / (66.0 * 16))
            note.fill(random.randint(44100, len(note)))
            note = note.env('phasor') * random.triangular(0.08, 0.2)
            note = note.pan(random.random())
            out.dub(note, pos + start)

    start += length

out.write('pulses.wav')

