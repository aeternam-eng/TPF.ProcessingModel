from flask import Flask, request
import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
import joblib
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return { "running": True }

@app.route('/api/analysis', methods=['POST'])
def fire_probability():
    def randomForest():
        randomForestModel = joblib.load('./modelo_random_forest.pkl')

        lat = request.form["lat"]
        lon = request.form["lon"]
        temp = request.form["temp"]
        umi = request.form["umi"]
        infoNames = ['lat', 'lon', 'temperatura', 'umidade']

        sensorData = np.array([[lat, lon, temp, umi]])
        sensorDataDataFrame = pd.DataFrame(sensorData, columns=infoNames)
        probability = randomForestModel.predict_proba(sensorDataDataFrame)

        return probability[0][1]


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
    interpreter.set_tensor(input_details[0]['index'], processed_image)

    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    classes = interpreter.get_tensor(output_details[0]['index'])

    return { 
            "isFogoBixo" : bool(max(classes[0][0], classes[0][2]) == max(classes[0])), 
            "fogo" : float(round(classes[0][0], 8)),
            "neutra" : float(round(classes[0][1], 8)),
            "fumaça" : float(round(classes[0][2], 8)),
            "environmentalFireProbability" : float(randomForest())
            }

if __name__ == '__main__':
    app.run()
