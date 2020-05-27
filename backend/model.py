import tensorflow as tf
keras = tf.keras
import os
import numpy as np
from pathlib import Path

print(tf.__version__)

class Dog_Classifier():
    def __init__(self):
        self._cwd = Path(os.getcwd())
        self._model = keras.models.load_model(os.path.join(self._cwd,'mobilenet_pvb.tf'))
        self._model_img_size = 160
        self._num_to_class = {1 : "Pug", 0 : "Bulldog"}

    def _load_img(self, img_path):
        targ_size = self._model_img_size
        img = keras.preprocessing.image.load_img(img_path, 
            target_size=(targ_size, targ_size, 3))
        x = keras.preprocessing.image.img_to_array(img)
        x = x/127.5 - 1
        x = np.expand_dims(x, axis=0)
        return x

    def _decode_predictions(self, pred, prob):
        dog_breed = self._num_to_class[pred[0][0]]
        if (dog_breed == "Pug"):
            prob = prob[0][0]
        else:
            prob = 1.0 - prob[0][0]
        
        return dog_breed, prob
    
    def make_prediction(self, img_path):
        img = self._load_img(img_path)
        prediction = self._model.predict_classes(img, batch_size=None)
        pred_prob = self._model.predict(img, batch_size=None)
        return self._decode_predictions(prediction, pred_prob)
    
    @property
    def cwd(self):
        return self._cwd
