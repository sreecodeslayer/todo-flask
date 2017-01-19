from flask import Flask, jsonify, render_template, url_for, request
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask_mongoengine import MongoEngine, DoesNotExist
from settings import db,app
from models import User
import bcrypt

# now get all the models from models.py ( this can be inside app.py)
# am just making it in models.py for readbility

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user):
	return User.objects.get(id=user)

# ------------------------------------------------------------------------------------
# 										Flask Login ends
# ------------------------------------------------------------------------------------
@app.route("/")
def index():
	return render_template('index.html')

@app.route("/login", methods=['POST'])
def login():
	params = request.get_json()
	print params
	try:
		user = User.objects.get(username=params['username'])
		if user.validate_login(user.password, params['password']):
			user_obj = User.objects.get(id=user.id)
			login_user(user_obj)
			return jsonify({'status': True})
	except DoesNotExist:
		return jsonify({'status': False})
	return jsonify({'status': False})

@app.route("/signup", methods=['POST'])
def signup():
	params = request.get_json()
	print params
	try:
		print 'try'
		data = User.objects.get(username=params['username'])
		return jsonify({'status': False})
	except DoesNotExist:
		print 'except'
		hashed_pass = bcrypt.hashpw(params['password'], bcrypt.gensalt())
		user_obj = User(username=params['username'])
		user_obj.set_password(params['password'])
		user_obj.save()
	return jsonify({'status':True})

@app.route("/logout", methods=['POST'])
def logout():
	logout_user()
	return jsonify({'status':True})

if __name__ == '__main__':
	app.run(debug=True, threaded=True, host='0.0.0.0')