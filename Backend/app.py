# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from model import sentence_corrector

app = Flask(__name__)
CORS(app)

@app.route("/correct", methods=["POST"])
def correct():
    data = request.get_json()
    text = data.get("text", "")
    corrected = sentence_corrector(text)
    return jsonify({"corrected": corrected})

if __name__ == "__main__":
    print("Starting server at http://127.0.0.1:5000")
    app.run(debug=True)
