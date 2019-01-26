from flask import Flask
from model import Dog_Classifier

app = Flask(__name__)
print("Loading model")
classifier = Dog_Classifier()
print("model loaded")
UPLOAD_FOLDER = classifier.cwd
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

