import  s01_reading as s1 ,s02_vectorization as s2 ,s03_DataPrepration as s3,s04_Modeling as s4 ,s05_Training as s5 ,conf as c
import tensorflow as tf ,time

model = s4.build_model(
  vocab_size = len(s1.vocab),
  embedding_dim=s4.embedding_dim,
  rnn_units=s4.rnn_units,
  batch_size=s3.BATCH_SIZE)

# Training step
EPOCHS = 1
optimizer = tf.train.AdamOptimizer()

for epoch in range(EPOCHS):
    start = time.time()

    # initializing the hidden state at the start of every epoch
    # initially hidden is None
    hidden = model.reset_states()

    for (batch_n, (inp, target)) in enumerate(s3.dataset):
          with tf.GradientTape() as tape:
              # feeding the hidden state back into the model
              # This is the interesting step
              predictions = model(inp)
              loss = tf.losses.sparse_softmax_cross_entropy(target, predictions)

          grads = tape.gradient(loss, model.trainable_variables)
          optimizer.apply_gradients(zip(grads, model.trainable_variables))

          if batch_n % 100 == 0:
              template = 'Epoch {} Batch {} Loss {:.4f}'
              print(template.format(epoch+1, batch_n, loss))

    # saving (checkpoint) the model every 5 epochs
    if (epoch + 1) % 5 == 0:
      model.save_weights(s5.checkpoint_prefix.format(epoch=epoch))

    print ('Epoch {} Loss {:.4f}'.format(epoch+1, loss))
    print ('Time taken for 1 epoch {} sec\n'.format(time.time() - start))

model.save_weights(s5.checkpoint_prefix.format(epoch=epoch))