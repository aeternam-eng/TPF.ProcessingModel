from flask import Flask, request
import numpy as np
import keras 
import tflite_runtime.interpreter as tflite
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['POST'])
def health_check():
    return { "running": True }

@app.route('/api/analysis', methods=['POST'])
def fire_probability():
    model = tflite.Interpreter(model_path='./TPF.tflite')

    file = request.files['file']

    img = Image.open(file.stream)
    img = img.resize((224,224),Image.ANTIALIAS)

    x = keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0) /255

    classes = model.predict(x)
    result = np.argmax(classes[0])==0, max(classes[0])

    return { 
        "isFogoBixo": bool(result[0]),
        "probability": float(result[1])
    }

if __name__ == '__main__':
    app.run()
