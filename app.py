from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({'message':'Backend is up!'})

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')