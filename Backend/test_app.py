from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/correct', methods=['POST'])
def correct():
    data = request.get_json()
    return jsonify({"received": data})

if __name__ == '__main__':
    app.run(debug=True)
