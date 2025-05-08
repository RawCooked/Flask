from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Ensure the uploads directory is created (temporary in Render)
UPLOAD_FOLDER = '/tmp/uploads/'  # Render provides a /tmp directory for temporary storage
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'message': 'Image uploaded successfully', 'filename': filename}), 200

@app.route('/uploads/<filename>', methods=['GET'])
def get_image(filename):
    try:
        # Serve the uploaded file from the /tmp/uploads/ directory
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/', methods=['GET'])
def home():
    return 'Image Upload API is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
