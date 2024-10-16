# Late Show API

## Overview

The Late Show API is a RESTful web service built with Flask, designed to manage and retrieve information about episodes, guests, and their appearances on a fictional late-night show. This API allows users to interact with a database containing details about episodes, guests, and their ratings for each appearance, offering a seamless experience for developers and end-users alike.

**TABLE OF CONTENT**
- [Late Show API](#late-show-api)
  - [Overview](#overview)
  - [Purpose](#purpose)
  - [Usage](#usage)
  - [Program Requirements](#program-requirements)
    - [Installation Process](#installation-process)
  - [Models Overview](#models-overview)
    - [Guest Model:](#guest-model)
    - [Episode Model:](#episode-model)
    - [Appearance Model:](#appearance-model)
  - [Conclusion](#conclusion)
## Purpose

The primary purpose of this API is to provide an easy-to-use interface for managing show data. It supports operations such as retrieving episode and guest information, adding appearances, and deleting episodes. This API can be utilized for developing client applications that require access to show-related data.

## Usage

This API supports the following operations:
- Retrieve a list of episodes.
- Get details of a specific episode by ID, including guest appearances.
- Retrieve a list of guests.
- Add a new appearance record for a guest in an episode.
- Delete an episode by ID.

## Program Requirements

Before running the program, ensure you have the following installed:

- Python 3.8+
- Flask
- Werkzeug
- Importlib-metadata
- Importlib-resources
- Flask-SQLAlchemy
- Flask-Migrate
- SQLAlchemy-Serializer

### Installation Process

1. **Clone the repository to your local machine** by using the link below;
   ```bash
   git@github.com:NjaiSamson/late-show-code-challenge.git
   ```
   
2. **Install pipenv** (if not installed): 
   ```bash
   pip install pipenv
   ```
3. **Install dependencies**. Use pipenv to install the required packages from the Pipfile using the following command:
   ```bash
   pipenv install
   ```
4. **Activate the virtual environment** by using the following command
   ```bash
   pipenv shell
   ````
5. **Navigate to the server directory** by using the command
   ```bash
   cd server
   ```
6. **Run the migrations** to set up the schema using the following commands:
   ```bash
   flask db init
   ```
   ```bash
   flask db migrate -m "initial migration"
   ```
   ```bash
   flask db upgrade head
   ```

7. **Set up Flask environment variables**  by running the following commands:
   ```bash
   export FLASK_APP=app.py
   ```
   ```bash
   export FLASK_RUN_PORT=5555
   ```
8. **Populate the database with seed data** by running the seed.py file:
   ```bash
   python seed.py
   ```
9.  **Run the application to test different endpoints**
    ```bash
    python app.py
    ```
10. **Access the application using the following routes endpoints**.
    
    **Homepage endpoint**
    ```bash
    http://localhost:5555
    ```
    **List of episodes endpoint**
     ```bash
    http://localhost:5555/episodes
    ```
    ```json
    {
        "id": 1,
        "date": "1/11/99",
        "number": 1
    },
    {
        "id": 2,
        "date": "1/12/99",
        "number": 2
    }
    ```

    **Each episode by id endpoint. Replace <<int:id>> with the actual episode id**
     ```bash
    http://localhost:5555/episodes/<int:id>
    ```
    ```json
    {
        "id": 1,
        "date": "1/11/99",
        "number": 1,
        "appearances": [
            {
                "episode_id": 1,
                "guest": {
                    "id": 1,
                    "name": "Michael J. Fox",
                    "occupation": "actor"
                },
                "guest_id": 1,
                "id": 1,
                "rating": 4
            }
        ]
        }
    ```
    
    **List of guests endpoint**
     ```bash
    http://localhost:5555/guests
    ```
    ```json
        {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
        },
        {
            "id": 2,
            "name": "Sandra Bernhard",
            "occupation": "Comedian"
        },
        {
            "id": 3,
            "name": "Tracey Ullman",
            "occupation": "television actress"
        }
    ```
    **Posting appearances endpoint**
     ```bash
    http://localhost:5555/appearances
    ```
    ```json 
        {
        "id": 162,
        "rating": 5,
        "guest_id": 3,
        "episode_id": 2,
        "episode": {
            "date": "1/12/99",
            "id": 2,
            "number": 2
        },
        "guest": {
            "id": 3,
            "name": "Tracey Ullman",
            "occupation": "television actress"
        }
        }
    ```

## Models Overview
### Guest Model:
- Represents a guest with a unique id, name, and occupation.
- Relationship: A guest can have multiple appearances linked to different episodes through the Appearance model.
  
### Episode Model:
- Represents an episode with a unique id, date, and number.
- Relationship: An episode can have multiple appearances, each associated with different guests, through the Appearance model.
  
### Appearance Model:
- Represents the relationship between guests and episodes, capturing the details of each appearance.
- Contains id, rating (from 1 to 5), guest_id, and episode_id.
- Links the guest_id and episode_id to their respective Guest and Episode models, allowing for a many-to-many relationship between guests and episodes.

## Conclusion
The Late Show API serves as a robust backend service for managing and retrieving information about episodes, guests, and their appearances. With a clear structure and RESTful principles, it enables developers to easily integrate show data into their applications. By following the installation and usage guidelines, you can quickly set up and utilize the API for your development needs. For any issues or contributions, feel free to open an issue or submit a pull request in the repository.