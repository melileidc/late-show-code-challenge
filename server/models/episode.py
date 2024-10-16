from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from utils.dbconfig import db

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    
    # Limit recursion 
    serialize_rules = ('-guests.episode',)
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    # Relationship mapping guest to related episode
    guests = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')
    
    
    
    # validating date
    @validates('date')
    def validate_date(self, key, date):
        if not date or date.strip() == '':
            raise ValueError("Date field must be a string and cannot be empty.")
        
        # Check if date is a string
        if not isinstance(date, str):
            raise ValueError("Number must be an a string.")        
        return date
    
    # Validating the number
    @validates('number')
    def validate_number(self, key, number):
        if number is None:
            raise ValueError("Number field cannot be empty.")
        
        # Check if number is an integer
        if not isinstance(number, int):
            raise ValueError("Number must be an integer.")
        
        return number
    
    def __repr__(self):
        return f'Episode  {self.number} for date {self.date}'  