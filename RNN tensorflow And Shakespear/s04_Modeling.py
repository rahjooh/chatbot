import s01_reading as s1 , s02_vectorization as s2,s03_DataPrepration as s3 ,conf as c
import tensorflow as tf

# Length of the vocabulary in chars
vocab_size = len(s1.vocab)

# The embedding dimension
embedding_dim = 256

# Number of RNN units
rnn_units = 1024

if tf.test.is_gpu_available():
  rnn = tf.keras.layers.CuDNNGRU
else:
  import functools
  rnn = functools.partial(
    tf.keras.layers.GRU, recurrent_activation='sigmoid')


def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
  model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim,
                              batch_input_shape=[batch_size, None]),
    rnn(rnn_units,
        return_sequences=True,
        recurrent_initializer='glorot_uniform',
        stateful=True),
    tf.keras.layers.Dense(vocab_size)
  ])
  return model


model = build_model(
  vocab_size = len(s1.vocab),
  embedding_dim=embedding_dim,
  rnn_units=rnn_units,
  batch_size=s3.BATCH_SIZE)

for input_example_batch, target_example_batch in s3.dataset.take(1):
  example_batch_predictions = model(input_example_batch)
  if c.report_s04 :
      print(example_batch_predictions.shape, "# (batch_size, sequence_length, vocab_size)")


if c.report_s04 :
    print('model summary : \n',model.summary())

sampled_indices = tf.random.categorical(example_batch_predictions[0], num_samples=1)
sampled_indices = tf.squeeze(sampled_indices,axis=-1).numpy()

if c.report_s04 :
    print('sample indices : \n', sampled_indices)

    print("Input: \n", repr("".join(s2.idx2char[input_example_batch[0]])))
    print()
    print("Next Char Predictions: \n", repr("".join(s2.idx2char[sampled_indices ])))