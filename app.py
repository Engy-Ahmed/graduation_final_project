from flask import Flask, request, render_template, jsonify
import os
import tensorflow as tf
import numpy as np

app = Flask(__name__)
\
# Load the trained model
model = tf.keras.models.load_model('melanoma_model.h5')

# Directories
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    # Check if the file has an allowed extension
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page route
@app.route('/')
def home():
    # Render the index.html template
    return render_template('index.html')

# Predict route for cancer type prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        # Error if no file part in the request
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        # Error if no file selected
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        # Save the uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Preprocess the image
        img = tf.keras.preprocessing.image.load_img(filepath, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch
        
        # Make predictions using the model
        predictions = model.predict(img_array)
        predicted_class = int(np.argmax(predictions[0]))
        
        # Return the predicted class
        return jsonify({'class': predicted_class})

    else:
        # Error for invalid file format
        return jsonify({'error': 'Invalid file format'})

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
