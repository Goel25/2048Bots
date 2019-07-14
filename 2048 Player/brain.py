import tensorflow as tf
import numpy as np
import random
import time


class Brain:
    def __init__(self, path):
        self.path = path
        self.model = tf.keras.Sequential()
        bias_init = tf.keras.initializers.random_normal()
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(16,
                                             bias_initializer=bias_init,
                                             activation="relu",
                                             input_shape=(16,)))
        self.model.add(tf.keras.layers.Dense(16,
                                             bias_initializer=bias_init,
                                             activation="relu"))
        self.model.add(tf.keras.layers.Dense(4,
                                             bias_initializer=bias_init,
                                             activation="softmax"))
        self.model.compile(optimizer=tf.train.AdamOptimizer(0.001),
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])

    def train(self, x, y, e):
        self.model.fit([x], [y],
                       batch_size=32,
                       epochs=e,
                       shuffle=True)

    def predict(self, inp):
        inp = sum(inp, [])
        largest = max(inp)
        for i in range(len(inp)):
            inp[i] /= largest  # Normalize values
        inp = np.array([inp])  # convert to numpy array
        result = self.model.predict(inp, batch_size=32)
        # highest_index = np.argmax(result)
        return result

    def save_model(self):
        t = time.localtime()
        day = t.tm_mday
        hour = t.tm_hour
        minutes = t.tm_min
        sec = t.tm_sec
        time_str = f"Model on the {day} at {hour}:{minutes}:{sec}.h5"
        self.model.save(f"{self.path}/models/{time_str}")

    def load_best(self):
        self.model = tf.keras.models.load_model(
            "2048Bot/models/Best model.h5")
