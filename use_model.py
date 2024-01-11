import numpy as np
import tensorflow as tf

trained_model = tf.keras.models.load_model('trained_model.keras')

def use_model(sample_text):
    p = trained_model.predict(np.array([sample_text]))
    return p