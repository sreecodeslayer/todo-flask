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
	try:
		user = User.objects.get(id=current_user.id)
		return render_template('index.html', username = current_user.username)
	except (AttributeError, DoesNotExist):
		return render_template('index.html', username = False)

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
		hashed_pass = bcrypt.hashpw(str(params['password']), bcrypt.gensalt())
		user_obj = User(username=params['username'])
		user_obj.set_password(params['password'])
		user_obj.save()
	return jsonify({'status':True})

@app.route("/logout", methods=['POST'])
def logout():
	logout_user()
	return jsonify({'status':True})

# ------------------------------------------------------------------------------------------------
# 										TASK CRUDs
# ------------------------------------------------------------------------------------------------
# CREATE
@app.route("/new", methods=['POST'])
@login_required
def new_task():
	data = request.get_json()
	# Add new task for the user
	return jsonify({'status':True})

# UPDATE
@app.route("/edit", methods=['POST'])
@login_required
def edit_task():
	data = request.get_json()
	# Edit the particular task
	return jsonify({'status':True})

# DELETE
@app.route("/delete", methods=['POST'])
@login_required
def delete_task():
	data = request.get_json()
	# Delete the particular task
	return jsonify({'status':True})

# ALL TASKS
@app.route("/tasks", methods=['GET'])
@login_required
def get_tasks():
	data = request.get_json()
	# Return all the tasks created by the <user>
	return jsonify({'status':True,'tasks':tasks})

if __name__ == '__main__':
	app.run(debug=True, threaded=True, host='0.0.0.0')