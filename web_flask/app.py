#!/usr/bin/python3

"""app module"""

from flask import Flask
from home import app_views_home
from action import app_views_action
from property import app_views_property


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'


app.register_blueprint(app_views_home)
app.register_blueprint(app_views_action)
app.register_blueprint(app_views_property)


if __name__ == "__main__":
    app.run(debug=True)
