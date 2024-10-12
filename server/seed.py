from app import app
from models import db, Episode, Guest, Appearance
from datetime import date

# Function to seed the database
def seed_data():
    with app.app_context():  # Creating application context
        # Clearing existing data
        db.drop_all()
        db.create_all()

        # Creating sample episodes
        episodes = [
            Episode(date=date(1999, 11, 1), number=1),
            Episode(date=date(1999, 12, 1), number=2),
            Episode(date=date(2000, 1, 1), number=3),
            Episode(date=date(2000, 2, 1), number=4),
            Episode(date=date(2000, 3, 1), number=5),
        ]

        # Adding episodes to the session
        db.session.add_all(episodes)
        print("Database seeded with episodes!")

        # Creating sample guests
        guests = [
            Guest(name="Michael J. Fox", occupation="actor"),
            Guest(name="Sandra Bernhard", occupation="Comedian"),
            Guest(name="Tracey Ullman", occupation="television actress"),
            Guest(name="Steve Carell", occupation="actor"),
            Guest(name="Amy Poehler", occupation="comedian"),
        ]

        # Adding guests to the session
        db.session.add_all(guests)
        print("Database seeded with guests!")

        # Creating sample appearances with ratings
        appearances = [
            Appearance(rating=4, episode=episodes[0], guest=guests[0]),
            Appearance(rating=5, episode=episodes[1], guest=guests[2]),
            Appearance(rating=3, episode=episodes[2], guest=guests[1]),
            Appearance(rating=4, episode=episodes[3], guest=guests[3]),
            Appearance(rating=2, episode=episodes[4], guest=guests[4]),
        ]

        # Adding appearances to the session
        db.session.add_all(appearances)
        print("Database seeded with appearances!")

        # Committing the session to the database
        db.session.commit()
        print("Database seeded successfully!!!!!!!!!!!!!!!")

if __name__ == '__main__':
    seed_data()
