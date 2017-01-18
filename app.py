from flask import Flask, jsonify, render_template, url_for
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')