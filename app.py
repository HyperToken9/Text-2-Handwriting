
from flask import Flask, request, send_from_directory, jsonify, send_file
from flask_cors import CORS, cross_origin

import sys
import os
import shutil

from backend import HandwritingFunctions

app = Flask(__name__, 
            static_folder= os.path.join("handwriting-frontend", 
                                        "build"),
            static_url_path='')
CORS(app)

@app.route('/api/generate-pages', methods=['POST'])
@cross_origin()
def generate_pages():
    
    data = request.get_json()
    text = data.get('text')

    shutil.rmtree(os.path.join("backend", "testing"), ignore_errors=True)
    HandwritingFunctions.WritePages("testing", text, "", [False, True, True])
    
    return {"message": "Success", "num_pages": len(os.listdir(os.path.join("backend", "testing"))) - 1}

@app.route('/api/get-page', methods=['GET'])
@cross_origin()
def get_page():
    try:
        num_pages = len(os.listdir(os.path.join("backend", "testing")))
        page_index = int(request.args.get('index', -1))
        print("Page Index: ", page_index)
        if page_index < 0 or page_index >= num_pages:
            return jsonify({"message": "Invalid page index", "num_pages": num_pages}), 400

        return send_from_directory(os.path.join('backend', 'testing'), f'{page_index}.jpg')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-pdf', methods=['GET'])
@cross_origin()
def get_pdf():

    try:
        directory = os.listdir(os.path.join("backend", "testing"))
        if 'testing.pdf' not in directory:
            return jsonify({"message": "PDF not generated"}), 400
        else:
            pdf_path = os.path.join('backend', 'testing', 'testing.pdf')
            return send_file(pdf_path, as_attachment=True)
            # return send_from_directory(os.path.join('backend', 'testing'), 'testing.pdf', as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run(debug=True)
