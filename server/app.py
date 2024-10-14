#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Episode, Appearance, Guest

# Creating Flask app instance
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///late_show.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  

# Initializing Flask-Migrate
migrate = Migrate(app, db)

# Initializing the database with the app context
db.init_app(app)

# Routes

# Home route
@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the Late Show API!</h1>"

# Route to get all episodes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    episodes_list = [
        {
            "id": episode.id,
            "date": episode.date.strftime('%-m/%-d/%y'),
            "number": episode.number
        } for episode in episodes
    ]
    return jsonify(episodes_list), 200

# Route to get a specific episode by ID
@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    
    if episode is None:
        return jsonify({"error": "Episode not found"}), 404
    
    episode_data = {
        "id": episode.id,
        "date": episode.date.strftime('%-m/%-d/%y'),
        "number": episode.number,
        "appearances": [
            {
                "id": appearance.id,
                "episode_id": appearance.episode_id,
                "guest_id": appearance.guest_id,
                "rating": appearance.rating,
                "guest": {
                    "id": appearance.guest.id,
                    "name": appearance.guest.name,
                    "occupation": appearance.guest.occupation
                }
            } for appearance in episode.appearances
        ]
    }
    
    return jsonify(episode_data), 200

# Route to get all guests
@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    guests_list = [
        {
            "id": guest.id,
            "name": guest.name,
            "occupation": guest.occupation
        } for guest in guests
    ]
    return jsonify(guests_list), 200

# Route to create a new appearance
@app.route('/appearances', methods=['POST'])
def create_appearance():
    try:
        data = request.get_json()

        # Initializing error messages
        errors = []

        # Checking if episode ID is provided and valid
        episode_id = data.get('episode_id')
        if episode_id is None:
            errors.append("Episode ID is required.")
        else:
            episode = Episode.query.get(episode_id)
            if not episode:
                errors.append("The specified episode does not exist.")

        # Checking if guest ID is provided and valid
        guest_id = data.get('guest_id')
        if guest_id is None:
            errors.append("Guest ID is required.")
        else:
            guest = Guest.query.get(guest_id)
            if not guest:
                errors.append("The specified guest does not exist.")

        # If there are errors, return them
        if errors:
            return jsonify({"errors": errors}), 404

        # Creating new appearance with validated rating
        new_appearance = Appearance(
            rating=data.get('rating'),
            episode_id=episode.id,
            guest_id=guest.id
        )

        # Adding and commit the new appearance
        db.session.add(new_appearance)
        db.session.commit()

        # Preparing response data
        appearance_data = {
            "id": new_appearance.id,
            "rating": new_appearance.rating,
            "guest_id": new_appearance.guest_id,
            "episode_id": new_appearance.episode_id,
            "episode": {
                "id": episode.id,
                "date": episode.date.strftime('%-m/%-d/%y'),
                "number": episode.number
            },
            "guest": {
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation
            }
        }

        return jsonify(appearance_data), 201

    except ValueError as e:
        # Handling validation errors (like rating out of range)
        return jsonify({"errors": [str(e)]}), 400

    except Exception as e:
        # Handling other unforeseen errors
        return jsonify({"errors": ["Something went wrong."]}), 500

# Route to delete an episode by ID
@app.route('/episodes/<int:id>', methods=['DELETE'])
def delete_episode(id):
    episode = Episode.query.get(id)

    if episode is None:
        return jsonify({"error": "Episode not found"}), 404

    # Deleting the episode and its related appearances
    db.session.delete(episode)
    db.session.commit()

    return jsonify({"message": "Episode deleted successfully"}), 200

# Running the application
if __name__ == '__main__':
    app.run(host='0.0.0.0')
