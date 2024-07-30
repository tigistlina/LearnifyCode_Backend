import pytest
import os
from app import create_app
from firebase_admin import firestore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope='session')
def app():
    # Set up the Flask app with Firestore emulator configuration
    app = create_app(testing=True)
    yield app


@pytest.fixture(scope='session')
def client(app):
    # Set up a test client for making requests to the Flask app
    return app.test_client()


@pytest.fixture(scope='function')
def setup_firestore_emulator(app):
    # Get Firestore instance from app
    db = app.db

    # Define test lesson data
    test_lesson_data = {
        "prompt": "Explain the concept of dynamic programming",
        "lesson": [
            "Dynamic programming is a method used in computer science and mathematics to solve complex problems by breaking them down into smaller, more manageable subproblems. It involves solving each subproblem only once and storing the results, so that they can be reused in solving larger subproblems.",
            "",
            "The key idea behind dynamic programming is to solve a problem by considering all possible choices at each decision point and making an optimal choice based on the results of the subproblems that have already been solved. This approach can lead to significant improvements in efficiency and can enable the solution of problems that would be impractical or impossible to solve using a brute-force approach.",
            "",
            "Dynamic programming is commonly used in a variety of applications such as optimization, scheduling, and sequence alignment. It is particularly well-suited for problems"
        ]
    }

    # Add test data to Firestore
    test_id = 'test_id'
    db.collection('lessons').document(test_id).set(test_lesson_data)

    yield

    # Cleanup logic
    docs = db.collection('lessons').stream()
    for doc in docs:
        doc.reference.delete()
