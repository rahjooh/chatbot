import s01_reading as s1 , conf as c
import numpy as np

if c.report_s02:print('\n Process the Text : Vectorize the text ')
# Creating a mapping from unique characters to indices
char2idx = {u: i for i, u in enumerate(s1.vocab)}
idx2char = np.array(s1.vocab)

text_as_int = np.array([char2idx[c] for c in s1.text])

if c.report_s02:
    print('     {')
    for char, _ in zip(char2idx, range(20)):
        print('      {:4s}: {:3d},'.format(repr(char), char2idx[char]))
    print('  ...\n}')
    # Show how the first 13 characters from the text are mapped to integers
    print('     {} ---- characters mapped to int ---- > {}'.format(repr(s1.text[:13]), text_as_int[:13]))
