import pytest
from app.main import app
import os

@pytest.fixture
def client():
    # Enable testing mode in Flask
    app.config['TESTING'] = True

    # Set the new upload folder path in the test environment
    app.config['UPLOAD_FOLDER'] = '../app/uploads'

    # Ensure the folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    with app.test_client() as client:
        yield client


def test_predict_no_file(client):
    """Test the predict endpoint without an image file"""
    response = client.post('/predict')
    json_data = response.get_json()

    assert response.status_code == 400
    assert 'error' in json_data
    assert json_data['error'] == 'No image part in the request'

def test_predict_valid_file(client):
    """Test the predict endpoint with a valid image file"""
    with open('test_image.jpg', 'rb') as image_file:
        data = {
            'image': (image_file, 'test_image.jpg')
        }
        response = client.post('/predict', data=data, content_type='multipart/form-data')
        json_data = response.get_json()

        assert response.status_code == 202
        assert 'task_id' in json_data

# Example of different size/resolution test cases
@pytest.mark.parametrize("image_file", [
    ('resized_image_100x100.png'),  # Small image
    ('resized_image_640x640.png'),  # Medium image
    ('resized_image_1024x1024.jpg')  # Large image
])
def test_predict_image_sizes(client, image_file):
    """Test the predict endpoint with different image sizes and resolutions"""
    with open(image_file, 'rb') as img:
        data = {
            'image': (img, image_file)
        }
        response = client.post('/predict', data=data, content_type='multipart/form-data')
        json_data = response.get_json()

        assert response.status_code == 202
        assert 'task_id' in json_data
