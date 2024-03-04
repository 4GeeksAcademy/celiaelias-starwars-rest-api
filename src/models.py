from flask_sqlalchemy import SQLAlchemy
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
db = SQLAlchemy()
Base = declarative_base()

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True, default=True)

    def __repr__(self):
        return '<user %r>' % self.first_name

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "email": self.email
            # do not serialize the password, its a security breach
        }

class character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    gender = db.Column(db.String(80))
    affiliation = db.Column(db.String(150))

    def __repr__(self):
        return '<name %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

class planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    mass = db.Column(db.Float)
    diameter = db.Column(db.Float)
    atmosphere = db.Column(db.Float)
    orbital_period_year = db.Column(db.Float)
    orbital_period_day = db.Column(db.Float)

    def __repr__(self):
        return '<planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class favourite_characters(db.Model):
    __tablename__ = 'favourite_characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship(character)

    def __repr__(self):
        return '<user %r>' % self.character_id

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }

class favourite_planets(db.Model):
    __tablename__ = 'favourite_planets'
    id = Column(Integer, primary_key=True)
    user_id = Column(db.Integer, db.ForeignKey('User.id'))
    user = relationship(User)
    planet_id = Column(db.Integer, db.ForeignKey('planet.id'))
    planet = relationship('planet')

    def _repr_(self):
        return f'<FavouritePlanets {self.planet_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

