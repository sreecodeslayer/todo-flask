from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask_mongoengine import MongoEngine, DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash
from settings import db
import datetime

# Database Modals
class User(UserMixin, db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	username = db.StringField(max_length=255, required=True)
	password = db.StringField(max_length=255, required=True)

	def __unicode__(self):
		return self.id

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	@staticmethod
	def validate_login(password_hash, password):
		return check_password_hash(password_hash, password)

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'username'],
		'ordering': ['-created_at']
	}

class Task(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	user = db.ReferenceField(User)
	task_id = db.StringField(max_length=255, required=True)
	task_title = db.StringField(max_length=50, required=True)
	task_content = db.StringField(max_length=255, required=True)
