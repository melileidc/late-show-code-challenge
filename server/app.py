from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_migrate import Migrate

# models importations
from models.guest import Guest
from models.episode import Episode
from models.appearance import Appearance

# db configuration importation
from utils.dbconfig import db

# Configuring the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True 

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Homepage route
class HomePage(Resource):
    def get(self):
        response_dict = {"message": "Welcome to the Late Show API",}
        response = make_response(response_dict, 200)
        return response
api.add_resource(HomePage, '/')

class Episodes(Resource):
    # Getting episodes
    def get(self):
        episode_list = []
        for episode in Episode.query.all():
            episode_list.append({
                "id": episode.id,
                "date": episode.date,
                "number": episode.number                
            })
            response = make_response(episode_list, 200,
        )
        return response

api.add_resource(Episodes, '/episodes')

class EpisodeByID(Resource):
    def get(self, id):
        # Fetch the episode by its id, including appearances and related guests
        episode = Episode.query.filter_by(id=id).first()

        if not episode:
            return make_response(jsonify({"errors": ["Episode not found"]}), 404)

        # Prepare the appearances data
        appearances_list = []
        for appearance in episode.guests:  # 'guests' is the relationship in Episode model
            appearances_list.append({
                "id": appearance.id,
                "rating": appearance.rating,
                "episode_id": appearance.episode_id,
                "guest_id": appearance.guest_id,
                "guest": {
                    "id": appearance.guest.id,
                    "name": appearance.guest.name,
                    "occupation": appearance.guest.occupation
                }
            })

        # Prepare the response data
        response_dict = {
            "id": episode.id,
            "date": episode.date,
            "number": episode.number,
            "appearances": appearances_list
        }

        # Return the response
        return make_response(jsonify(response_dict), 200)
    
    def delete(self, id):
        # Fetch the episode by its id
        episode = Episode.query.filter_by(id=id).first()

        if not episode:
            return make_response(jsonify({"errors": ["Episode not found"]}), 404)

        try:
            # Delete the episode 
            db.session.delete(episode)
            db.session.commit()
            return make_response(jsonify({"message": "Episode deleted successfully"}), 200)

        except Exception as e:
            db.session.rollback()  
            return make_response(jsonify({"errors": [str(e)]}), 500)

api.add_resource(EpisodeByID, '/episodes/<int:id>')


# Guests route
class Guests(Resource):
    # Getting guests
    def get(self):
        guest_list = []
        for guest in Guest.query.all():
            guest_list.append({
                "id": guest.id,
                "name": guest.name,
                "occupation": guest.occupation                
            })
            response = make_response(guest_list, 200,
        )
        return response

api.add_resource(Guests, '/guests')

# Appearance posting route
class Appearances(Resource):
    def post(self):
        try:
            # Collecting data form the user form
            rating = request.form.get('rating')
            guest_id = request.form.get('guest_id')
            episode_id = request.form.get('episode_id')

            # Validate required fields
            if not rating or not guest_id or not episode_id:
                return make_response(jsonify({"errors": ["Missing required fields"]}), 400)

            # Convert guest_id, episode_id, and rating to integers
            try:
                rating = int(rating)
                guest_id = int(guest_id)
                episode_id = int(episode_id)
            except ValueError:
                return make_response(jsonify({"errors": ["guest_id, episode_id, and rating must be integers"]}), 400)

            # Validate rating before checking for duplicates
            if rating < 1 or rating > 5:
                return make_response(jsonify({"errors": ["Rating must be between 1 and 5"]}), 400)

            # Fetch episode and guest from the database
            episode = Episode.query.filter_by(id=episode_id).first()
            guest = Guest.query.filter_by(id=guest_id).first()

            if not episode:
                return make_response(jsonify({"errors": ["Episode not found"]}), 404)
            if not guest:
                return make_response(jsonify({"errors": ["Guest not found"]}), 404)

            # Checking for duplicates
            duplicate_appearance = Appearance.query.filter_by(guest_id=guest_id, episode_id=episode_id).first()
            if duplicate_appearance:
                return make_response(jsonify({"errors": ["Duplicate appearance for the guest and episode on this date"]}), 400)

            # Create a new Appearance record
            new_appearance = Appearance(
                rating=rating,
                guest_id=guest_id,
                episode_id=episode_id
            )
            db.session.add(new_appearance)
            db.session.commit()

            # Response data
            response_data = {
                "id": new_appearance.id,
                "rating": new_appearance.rating,
                "guest_id": guest.id,
                "episode_id": episode.id,
                "episode": {
                    "date": episode.date,
                    "id": episode.id,
                    "number": episode.number
                },
                "guest": {
                    "id": guest.id,
                    "name": guest.name,
                    "occupation": guest.occupation
                }
            }
            return make_response(jsonify(response_data), 201)

        # Handle validation errors
        except ValueError as e:            
            return make_response(jsonify({"errors": [str(e)]}), 400)

        except Exception as e:
            return make_response(jsonify({"errors": [str(e)]}), 500)

api.add_resource(Appearances, '/appearances')


if __name__ == '__main__':
    app.run(port=5555, debug=True)