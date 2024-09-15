import pytest
from app.main import app
import os
import time
import shutil

@pytest.fixture
def client():
    # Enable testing mode in Flask
    app.config['TESTING'] = True

    app.config['UPLOAD_FOLDER'] = '../app/uploads'

    # Ensure the folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    with app.test_client() as client:
        yield client
    # Cleanup code: Remove the weights folder after tests finish
    weights_folder = "weights"
    if os.path.exists(weights_folder):
        shutil.rmtree(weights_folder)


def count_persons(data):
    """Function to count persons from the result data"""
    persons = [obj for obj in data["result"] if obj["class_name"] == "person"]
    return len(persons)

def test_predict_no_file(client):
    """Test the predict endpoint without an image file"""
    response = client.post('/predict')
    json_data = response.get_json()

    assert response.status_code == 400
    assert 'error' in json_data
    assert json_data['error'] == 'No image part in the request'


def test_predict_valid_file(client):
    """Test the predict endpoint with a valid image file"""
    with open('images/test_image.jpg', 'rb') as image_file:
        data = {
            'image': (image_file, 'test_image.jpg')
        }
        response = client.post('/predict', data=data, content_type='multipart/form-data')
        json_data = response.get_json()

        assert response.status_code == 202
        assert 'task_id' in json_data

        # Check task status
        task_id = json_data['task_id']
        status_response = client.get(f'/result/{task_id}')
        status_json = status_response.get_json()

        assert status_response.status_code == 200
        assert status_json['status'] in ['Processing', 'Success', 'Failure']

#N persons test
@pytest.mark.parametrize("image_file, expected_count", [
    ('images/resized_image_100x100.jpg', 3),  # Small image, expect exactly 3 persons
    ('images/resized_image_640x640.jpg', 3),  # Medium image, expect exactly 3 persons
    ('images/resized_image_1024x1024.jpg', 4)  # Large image, expect exactly 4 persons
])
def test_predict_image_sizes(client, image_file, expected_count):
    """Test the predict endpoint with different image sizes and resolutions"""
    with open(image_file, 'rb') as img:
        data = {
            'image': (img, image_file)
        }
        response = client.post('/predict', data=data, content_type='multipart/form-data')
        json_data = response.get_json()

        assert response.status_code == 202
        assert 'task_id' in json_data

        # Check task status
        task_id = json_data['task_id']

        # Wait for a short time before checking the status (to simulate async task processing)
        time.sleep(5)

        status_response = client.get(f'/result/{task_id}')
        status_json = status_response.get_json()

        assert status_response.status_code == 200
        assert status_json['status'] == 'Success'

        # Count the number of persons in the result
        person_count = count_persons(status_json)
        print(f"Number of persons detected in {image_file}: {person_count}")

        # Assert that the model detected the exact number of persons
        assert person_count == expected_count


def test_predict_task_status(client):
    """Test the status of a task returned by the predict endpoint (General case)"""
    with open('images/test_image.jpg', 'rb') as image_file:
        data = {
            'image': (image_file, 'test_image.jpg')
        }
        response = client.post('/predict', data=data, content_type='multipart/form-data')
        json_data = response.get_json()

        assert response.status_code == 202
        assert 'task_id' in json_data

        task_id = json_data['task_id']

        # Wait for the task to finish (simulate waiting for async task)
        time.sleep(5)

        # Retrieve the task status
        status_response = client.get(f'/result/{task_id}')
        status_json = status_response.get_json()

        assert status_response.status_code == 200
        assert 'status' in status_json

        # Count the number of persons in the result
        person_count = count_persons(status_json)
        
        # Check the task result state
        assert status_json['status'] in ['Processing', 'Success', 'Failure']
        assert person_count == 7
