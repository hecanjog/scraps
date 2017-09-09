import glob
import shutil
import os

samples = sorted(glob.glob('manys/*.wav'))

for i, filename in enumerate(samples):
    if i+1 >= 382 and i+1 <= 395: 
        shutil.copy(filename, 'drums/kicks{}.wav'.format(i))

    if i+1 >= 440 and i+1 <= 453: 
        shutil.copy(filename, 'drums/snarelong{}.wav'.format(i))

    if i+1 >= 490 and i+1 <= 498: 
        shutil.copy(filename, 'drums/snarecrisp{}.wav'.format(i))

    if i+1 >= 284 and i+1 <= 345: 
        shutil.copy(filename, 'drums/hats{}.wav'.format(i))

    if i+1 >= 519 and i+1 <= 526: 
        shutil.copy(filename, 'drums/splash{}.wav'.format(i))

    if i+1 >= 594 and i+1 <= 598: 
        shutil.copy(filename, 'drums/ride{}.wav'.format(i))

    if i+1 >= 599 and i+1 <= 602: 
        shutil.copy(filename, 'drums/softride{}.wav'.format(i))

    if i+1 >= 527 and i+1 <= 535: 
        shutil.copy(filename, 'drums/softroll{}.wav'.format(i))

