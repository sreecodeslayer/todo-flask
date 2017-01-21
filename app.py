from flask import Flask, jsonify, render_template, url_for, request
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask_mongoengine import MongoEngine, DoesNotExist
from settings import db,app
from models import User, Task
import bcrypt
from uuid import uuid4

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

	try:

		data = User.objects.get(username=params['username'])
		return jsonify({'status': False})
	except DoesNotExist:

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

	try:
		task_obj = Task()
		task_obj.user = User.objects.get(id=current_user.id)
		task_obj.task_title = data['task_title']
		task_obj.task_content = data['task_content']
		task_obj.task_id = str(uuid4())
		task_obj.save()

		# Now get all task for this user and return it
		all_tasks = Task.objects(user = current_user.id).order_by('created_at','-created_at')
		his_tasks = []
		for task in all_tasks:
			his_tasks.append({
				'task_title':task.task_title,
				'task_content':task.task_content,
				'task_id':task.task_id
				})
		return jsonify({'status':True,'tasks':his_tasks})
	except Exception as e:

		return jsonify({'status':False})

# UPDATE
@app.route("/edit", methods=['POST'])
@login_required
def edit_task():
	data = request.get_json()
	# Edit the particular task

	try:
		task_obj = Task.objects.get(user = current_user.id, task_id = data['task_id'])
		task_obj.task_content = data['task_content']
		task_obj.task_title = data['task_title']
		task_obj.save()

		# Now get all task for this user and return it
		all_tasks = Task.objects(user = current_user.id).order_by('created_at','-created_at')
		his_tasks = []
		for task in all_tasks:
			his_tasks.append({
				'task_title':task.task_title,
				'task_content':task.task_content,
				'task_id':task.task_id
				})
		return jsonify({'status':True,'tasks':his_tasks})
	except DoesNotExist as e:

		return jsonify({'status':False})

# DELETE
@app.route("/delete", methods=['POST'])
@login_required
def delete_task():
	data = request.get_json()
	# Delete the particular task

	try:
		Task.objects.get(user = current_user.id, task_id = data['task_id']).delete()

		# Now get all task for this user and return it
		all_tasks = Task.objects(user = current_user.id).order_by('created_at','-created_at')
		his_tasks = []
		for task in all_tasks:
			his_tasks.append({
				'task_title':task.task_title,
				'task_content':task.task_content,
				'task_id':task.task_id
				})
		return jsonify({'status':True,'tasks':his_tasks})
	except DoesNotExist as e:

		return jsonify({'status':False})

# ALL TASKS
@app.route("/tasks", methods=['GET'])
@login_required
def get_tasks():
	# Return all the tasks created by the <user>
	try:
		all_tasks = Task.objects(user = current_user.id).order_by('created_at','-created_at')
		his_tasks = []
		for task in all_tasks:
			his_tasks.append({
				'task_title':task.task_title,
				'task_content':task.task_content,
				'task_id':task.task_id
				})

		return jsonify({'status':True,'tasks':his_tasks})
	except Exception as e:

		return jsonify({'status':False})

if __name__ == '__main__':
	app.run(debug=True, threaded=True, host='0.0.0.0')