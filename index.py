from flask import Flask, request, jsonify, send_file
import os
import shutil

app = Flask(__name__)

# Assume secar.py becomes a function
from main import calculate  # We'll define this function inside secar.py

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/calculate', methods=['POST'])
def calculate():
    file = request.files.get('file')
    
    if not file:
        return jsonify({'error': 'No file provided.'}), 400

    # Validate if the file is a text file
    if not file.filename.endswith('.txt') or file.mimetype != 'text/plain':
        return jsonify({'error': 'Only .txt files are accepted.'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, 'in.txt')
    file.save(file_path)

    # Copy to expected location for the script
    shutil.copy(file_path, 'in.txt')

    try:
        results = calculate()  # You need to adapt secar.py to provide this function
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results', methods=['GET'])
def get_results():
    if not os.path.exists('output.txt'):
        return jsonify({'error': 'No results yet. Please run /calculate first.'}), 400
    return send_file('output.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
