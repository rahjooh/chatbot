import s01_reading as s1 , s02_vectorization as s2 ,conf as c
import tensorflow as tf
tf.enable_eager_execution() # for iteration over dataset
tf.logging.set_verbosity(tf.logging.ERROR) # just for hiding warning

# The maximum length sentence we want for a single input in characters
seq_length = 100
examples_per_epoch = len(s1.text)//seq_length

# Create training examples / targets
char_dataset = tf.data.Dataset.from_tensor_slices(s2.text_as_int)

if c.report_s03 :
    for i in char_dataset.take(5):
        print(s2.idx2char[i.numpy()])

sequences = char_dataset.batch(seq_length+1, drop_remainder=True)

if c.report_s03 :
    for item in sequences.take(5):
      print(repr(''.join(s2.idx2char[item.numpy()])))

def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text

dataset = sequences.map(split_input_target)

if c.report_s03:
    for input_example, target_example in dataset.take(1):
        print('Input data: ', repr(''.join(s2.idx2char[input_example.numpy()])))
        print('Target data:', repr(''.join(s2.idx2char[target_example.numpy()])))
    for i, (input_idx, target_idx) in enumerate(zip(input_example[:5], target_example[:5])):
        print("Step {:4d}".format(i))
        print("  input: {} ({:s})".format(input_idx, repr(s2.idx2char[input_idx])))
        print("  expected output: {} ({:s})".format(target_idx, repr(s2.idx2char[target_idx])))


# Batch size
BATCH_SIZE = 64
steps_per_epoch = examples_per_epoch//BATCH_SIZE

# Buffer size to shuffle the dataset
# (TF data is designed to work with possibly infinite sequences,
# so it doesn't attempt to shuffle the entire sequence in memory. Instead,
# it maintains a buffer in which it shuffles elements).
BUFFER_SIZE = 10000

dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

if c.report_s03 : print(dataset)