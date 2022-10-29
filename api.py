from flask import Flask, request
import numpy as np
import keras 
import tensorflow as tf
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['POST'])
def fire_probability():
    model = tf.keras.models.load_model('./InceptionV3.h5')

    file = request.files['file']

    img = Image.open(file.stream)
    img = img.resize((224,224),Image.ANTIALIAS)

    x = keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0) /255

    classes = model.predict(x)
    result = np.argmax(classes[0])==0, max(classes[0])

    return{ "isFogoBixo" : bool(result[0]), "probability" : float(result[1]) }
app.run()