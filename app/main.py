from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from celery.result import AsyncResult
from worker import celery_app
from model.model import ObjectDetectionModel
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

model = ObjectDetectionModel()

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

        # Ensure the upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file.save(file_path)

        # Send task to Celery
        task = celery_app.send_task('worker.process_image_task', args=[file_path])

        return jsonify({'task_id': task.id}), 202
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PENDING':
        response = {
            'status': 'Processing'
        }
    elif task_result.state == 'SUCCESS':
        response = {
            'status': 'Success',
            'result': task_result.result
        }
    elif task_result.state == 'FAILURE':
        response = {
            'status': 'Failure',
            'detail': str(task_result.result)
        }
    else:
        response = {
            'status': task_result.state
        }
    return jsonify(response)

def allowed_file(filename):
    allowed_extensions = ['png', 'jpg', 'jpeg']
    extension = filename.split('.')[-1].lower()  
    return extension in allowed_extensions


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000)
