from flask import request, jsonify
from server import app, classifier, ALLOWED_EXTENSIONS
import os
from pathlib import Path
import tensorflow as tf

#graph = tf.get_default_graph()

@app.route('/')
def base():
    return "yeetdaddy we r in"

@app.route('/api/make_prediction', methods=['POST'])
def predict():
    response = {
        'Failed': True,
        'Prediction' : None,
        'Probability' : None,
        'Reason' : None
    }

    # Check if actual file was pinged through
    if 'image' not in request.files:
        response['Reason'] = "No file detected"
        return jsonify(response)

    uploaded_image = request.files['image']
    # Check if that the submitted file is real
    if uploaded_image.filename == '':
        response['Reason'] = "No file selected"
        return jsonify(response)

    print(uploaded_image.filename)
    # Check if is an image 
    if  not check_allowed(uploaded_image.filename):
        response['Reason'] = "Not a supported file format"
        return jsonify(response)

    # Save
    img_path = app.config['UPLOAD_FOLDER']/uploaded_image.filename
    uploaded_image.save(str(img_path))
    print(img_path)
    # Check if it is an image
    #global graph
    #with graph.as_default():
    prediction, probability = classifier.make_prediction(img_path)
    response["Prediction"] = prediction
    response["Probability"] = f'{probability:.2f}'
    response["Failed"] = False
    # Remove temp file
    print("Finished predicting")
    os.remove(img_path)

    # Pass back
    return jsonify(response)

def check_allowed(file_name):
    print(file_name.rsplit('.'))
    return '.' in file_name and \
        file_name.rsplit('.')[-1].lower() in ALLOWED_EXTENSIONS