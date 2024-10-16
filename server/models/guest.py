from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from utils.dbconfig import db

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'
    
    # Limit recursion 
    serialize_rules = ('-episodes.guest',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    
    # Relationship mapping the a guest to the related episodes
    episodes = db.relationship('Appearance', back_populates="guest", cascade='all, delete-orphan' )
    
    # Validates to ensure guest name is not empty
    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip() == '':
            raise ValueError("Guest must have a name")
        return name
    
    # Validates to ensure guest occupation firld is not empty
    @validates('occupation')
    def validate_occupation(self, key, occupation):
        if not occupation or occupation.strip() == '':
            raise ValueError("Guest occupation cannot be empty.")
        return occupation
    
    def __repr__(self):
        return f'Guest {self.name} with coocupation {self.occupation}'  