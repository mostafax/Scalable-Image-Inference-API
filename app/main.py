from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({'Message': 'Testing the API'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)