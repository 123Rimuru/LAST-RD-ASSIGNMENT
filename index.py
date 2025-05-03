from flask import Flask, request, jsonify, send_file
import os
import shutil
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Assume secar.py becomes a function
from main import calculateResults  # We'll define this function inside secar.py

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

    # Copy to expected location for the calculation script
    shutil.copy(file_path, 'in.txt')

    try:
        # Now collect all required variables
        lamdaByL = request.form.get('lamdaByL')
        length = request.form.get('length')
        bml = request.form.get('bml')
        breadth = request.form.get('breadth')
        draft = request.form.get('draft')

        # Check if all variables are provided
        if None in [lamdaByL, length, bml, breadth, draft]:
            return jsonify({'error': 'Missing one or more required parameters: lamdaByL, length, bml, breadth, draft.'}), 400

        # Convert variables to float
        lamdaByL = float(lamdaByL)
        length = float(length)
        bml = float(bml)
        breadth = float(breadth)
        draft = float(draft)
        # Pass everything to the calculations function
        results = calculateResults(lamdaByL, length, bml, breadth, draft)
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
