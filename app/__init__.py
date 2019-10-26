# app/__init__.py

from flask import Flask

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True