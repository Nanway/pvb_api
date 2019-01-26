from tensorflow.python.keras.applications.resnet50 import preprocess_input
from tensorflow.python.keras.models import load_model
from keras_preprocessing import image as Image
import os
import numpy as np
from pathlib import Path


class Dog_Classifier():
    def __init__(self):
        self._cwd = Path(os.getcwd())
        self._model = load_model(self._cwd/'trained_model.h5')
        self._model_img_size = 224
        self._num_to_class = {1 : "Pug", 0 : "Bulldog"}

    def _load_img(self, img_path):
        targ_size = self._model_img_size
        img = Image.load_img(img_path, 
            target_size=(targ_size, targ_size))
        x = Image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        x = x/255
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
        prediction = self._model.predict_classes(img)
        pred_prob = self._model.predict(img)
        return self._decode_predictions(prediction, pred_prob)
    
    @property
    def cwd(self):
        return self._cwd
