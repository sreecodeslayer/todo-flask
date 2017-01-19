from flask_mongoengine import MongoEngine
from flask import Flask

global db
global app
app = Flask(__name__)
db = MongoEngine()
app.config['MONGODB_DB'] = 'TODO'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017
app.config['MONGODB_USERNAME'] = ''
app.config['MONGODB_PASSWORD'] = ''
app.secret_key = "Am I being w@tched? Damn yes!"
db.init_app(app)
