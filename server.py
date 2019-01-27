from flask import Flask
from model import Dog_Classifier
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
print("Loading model")
classifier = Dog_Classifier()
print("model loaded")
UPLOAD_FOLDER = classifier.cwd
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

