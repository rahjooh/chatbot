import tensorflow as tf
import conf as c
path_to_file = tf.keras.utils.get_file('shakespeare.txt','https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt')
print(type(path_to_file))
# Read, then decode for py2 compat.
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')
# length of text is the number of characters in it
if c.report_s01:print('    Length of text: {} characters'.format(len(text)))

# Take a look at the first 250 characters in text
if c.report_s01:print(text[:250])

# The unique characters in the file
vocab = sorted(set(text))
if c.report_s01:print('    {} unique characters'.format(len(vocab)))
