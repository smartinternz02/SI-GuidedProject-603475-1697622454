from flask import Flask, render_template, request , jsonify

import tensorflow as tf
import cv2,imghdr, os
import numpy as np
from flask_cors import CORS 
import mysql.connector

app = Flask(__name__)
CORS(app)

def pred_img(img):
    im = cv2.imread(img)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    resize = tf.image.resize(im,(256,256))
    yhat = model.predict(np.expand_dims(resize/255,0))
    if (yhat >= 0.5):
        return "Real Art"
    else:
        return "AI Art"
 
 
model = tf.keras.models.load_model('my_model.keras')
    
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

 
@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    if image:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(filename)

        pred = pred_img(filename)
        
        return jsonify({'message': 'Image uploaded successfully', 'filename': image.filename, 'pred' : pred })
    else:
        return jsonify({'error': 'Failed to upload image'}), 500

if __name__ == "__main__":
    app.run(host='localhost' , port = 5000,debug=True)