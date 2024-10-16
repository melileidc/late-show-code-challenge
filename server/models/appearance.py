from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# imports db configaration from utils folder
from utils.dbconfig import db

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'
    
    # Limiting recursion 
    serialize_rules = ('-guest.episodes', '-episode.guests',)
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    
    # ForeignKey stores guest id and episode id
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    
    # Relationship mapping the episode to the related guest
    guest = db.relationship('Guest', back_populates="episodes")
    episode = db.relationship('Episode', back_populates="guests")
    
    # validating  if it is between 1 to 5
    @validates('rating')
    def validate_rating(self, key, rating):
        if rating is None:
            raise ValueError("Rating field cannot be empty.")
                
        # Check if rating is an integer
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer.")
        
        # Check if rating is withing the required limits
        if rating < 1 or rating > 5:
            raise ValueError(f"Rating must be between a nd 5")
        
        return rating       
        
    
    def __repr__(self):
        return f'Episode rating {self.rating} rate id {self.id}'  