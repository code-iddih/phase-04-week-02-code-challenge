from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, CheckConstraint
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# Defining naming convention for foreign keys
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initializing SQLAlchemy with metadata
db = SQLAlchemy(metadata=metadata)

# Episode Model
class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    serialize_rules = ('-appearances.episode', '-guests.episodes')

    id = db.Column(db.Integer, primary_key=True)  
    date = db.Column(db.Date, nullable=False)      
    number = db.Column(db.Integer, nullable=False)  

    # Relationship with Appearance
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')

    # Many-to-many relationship with Guest through Appearance
    guests = db.relationship('Guest', secondary='appearances', back_populates='episodes', overlaps='appearances')

    def __repr__(self):
        return f'<Episode {self.id}: Number {self.number}, Date {self.date}>'

# Guest Model
class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    serialize_rules = ('-appearances.guest', '-episodes.guests')

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String, nullable=False)    
    occupation = db.Column(db.String, nullable=False) 

    # Relationship with Appearance
    appearances = db.relationship('Appearance', back_populates='guest', cascade='all, delete-orphan')

    # Many-to-many relationship with Episode through Appearance
    episodes = db.relationship('Episode', secondary='appearances', back_populates='guests', overlaps='appearances')

    def __repr__(self):
        return f'<Guest {self.id}: Name {self.name}, Occupation {self.occupation}>'

# Appearance Model (association table)
class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)  
    rating = db.Column(db.Integer, nullable=False) 

    # Foreign Keys with cascade deletes
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id', ondelete='CASCADE'), nullable=False)  # Foreign key to episodes
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id', ondelete='CASCADE'), nullable=False)    # Foreign key to guests

    # Relationships with overlaps parameter
    episode = db.relationship('Episode', back_populates='appearances', overlaps='guests')
    guest = db.relationship('Guest', back_populates='appearances', overlaps='episodes')

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError('Rating must be between 1 and 5.')
        return value

    def __repr__(self):
        return f'<Appearance Episode ID {self.episode_id}, Guest ID {self.guest_id}, Rating {self.rating}>'
