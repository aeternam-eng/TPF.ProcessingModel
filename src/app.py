from concurrent.futures import process
from flask import Flask, request
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return { "running": True }

@app.route('/api/analysis', methods=['POST'])
def fire_probability():
    interpreter = tflite.Interpreter(model_path='./TPF.tflite')
    interpreter.allocate_tensors()

    file = request.files['file']

    img = Image.open(file.stream)
    img = img.resize((224, 224), Image.ANTIALIAS)

    processed_image = np.array(img)
    processed_image = np.expand_dims(processed_image, axis = 0) / 255
    processed_image = np.float32(processed_image)

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Test the model on random input data.
    input_shape = input_details[0]['shape']
    interpreter.set_tensor(input_details[0]['index'], processed_image)

    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    classes = interpreter.get_tensor(output_details[0]['index'])
    
    result = np.argmax(classes[0])==0, max(classes[0])

    return { 
        "isFogoBixo": bool(result[0]),
        "probability": float(result[1])
    }

if __name__ == '__main__':
    app.run()
