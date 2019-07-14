import tensorflow as tf
import numpy as np
import random
import time  # TODO REMOVE THIS
RATE = .03 * .001  # .005% mutation rate
MUTATE_MAX = 1
BY_VALUE = 0
BY_LIST = 1
CROSSOVER_METHOD = BY_VALUE


def mutate(x, r):
    if random.random() < r:
        # TODO WEIGHTS ARE CONSTRAINED BTWN 1 AND -1, IS THAT A PROBLEM?
        # print("m")
        return (random.random() * (MUTATE_MAX * 2)) - MUTATE_MAX
    return x


def mutate_all(x, r=RATE):
    # print("Mutating all")
    if isinstance(x, list) or isinstance(x, np.ndarray):
        for i in range(len(x)):
            x[i] = mutate_all(x[i], r)
        return x
    else:
        return mutate(x, r)


def zero_all(x):
    if isinstance(x, list) or isinstance(x, np.ndarray):
        for i in range(len(x)):
            x[i] = mutate_all(x[i])
        return x
    else:
        return 0


def crossover_list(l1, l2):
    if CROSSOVER_METHOD == BY_VALUE:
        new_list = l1.copy()
        for i in range(len(l1)):
            if random.random() < .5:
                new_list[i] = l2[i]
        return new_list
    else:
        if random.random() < .5:
            return l1
        else:
            return l2


def crossover_2d(l1, l2):
    for i in range(len(l1)):
        l1[i] = crossover_list(l1[i], l2[i])
    return l1


class Brain:
    def __init__(self):
        # bias_init = tf.keras.initializers.random_normal()
        st = time.time()
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Dense(16,
                                             #  bias_initializer=bias_init,
                                             activation="relu",
                                             input_shape=(16,)))
        self.model.add(tf.keras.layers.Dense(16,
                                             #  bias_initializer=bias_init,
                                             activation="relu"))
        self.model.add(tf.keras.layers.Dense(8,
                                             #  bias_initializer=bias_init,
                                             activation="relu"))
        self.model.add(tf.keras.layers.Dense(4,
                                             #  bias_initializer=bias_init,
                                             activation="softmax"))
        self.model.predict(np.zeros(shape=(1, 16)))
        # self.w = self.model.get_weights()
        # self.model.predict(np.zeros(shape=(1, 16)))
        print(f"Brain created in {time.time() - st}")

    def predict(self, inps, normalize_by):
        for i in range(len(inps)):  # For all inps
            inps[i] = sum(inps[i], [])  # Flatten array
            for j in range(len(inps[i])):
                inps[i][j] /= normalize_by  # Normalize values
        inp = np.array(inps)  # convert to numpy array
        result = self.model.predict(inp, batch_size=32)
        return result

    def set_weight(self, w):
        self.model.set_weights(w)

    def load_best(self):
        self.model = tf.keras.models.load_model(
            "2048Bot/models/Best model.h5")

    def get_rand_weights(self):
        return mutate_all(self.model.get_weights(), 1)
