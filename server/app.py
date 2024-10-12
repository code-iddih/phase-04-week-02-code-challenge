#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from models import db, Episode, Guest, Appearance 

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///late_show.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initializing Flask-Migrate
migrate = Migrate(app, db)

# Initializing the database with the app context
db.init_app(app)


# Running the application
if __name__ == '__main__':
    app.run(debug=True) 
