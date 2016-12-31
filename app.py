from flask import Flask, jsonify, render_template, url_for, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def login():
	params = request.get_json()
	print params
	return jsonify({'status':True})

@app.route("/signup", methods=['POST'])
def signup():
	params = request.get_json()
	print params
	return jsonify({'status':True})

@app.route("/logout", methods=['POST'])
def logout():
	return True

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')